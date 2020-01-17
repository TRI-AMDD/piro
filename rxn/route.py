import itertools
import scipy
import numpy as np
import plotly.express as px
import pandas as pd
import os
import json
from copy import deepcopy
from pymatgen import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram
from rxn.data import GASES, GAS_RELEASE, DEFAULT_GAS_PRESSURES
from rxn.utils import get_v, epitaxy, similarity, update_gases
from rxn import MP_API_KEY, RXN_FILES


# TODO: for elements and gases (references) - don't allow multiple entries
# TODO: for E_d, test q = max(q_phases) - max of q, assuming that would be the limiting step


class SynthesisRoutes:
    def __init__(self, target_entry_id, confine_to_icsd=True, confine_to_stables=True, hull_distance=np.inf,
                 simple_precursors=False, explicit_includes=None, allow_gas_release=False,
                 add_element=None, temperature=298, pressure=1,
                 entries=None, epitaxies=None, similarities=None, sigma=None, transport_constant=None):
        """
        Synthesis reaction route recommendations, derived semi-empirically using the Classical Nucleation Theory
            and high-throughput DFT data.
            Precursor_library, epitaxial matches and similarities are precomputed upon instantiation.
        Args:
            target_entry_id (str): Materials Project entry id for target material
            confine_to_icsd (bool): Use ICSD-sourced entries to find precursors. Defaults to True.
            confine_to_stables: Use stable entries only to find. Defaults to True.
            hull_distance (float): Use entries within this distance to hull (eV/atom). Can significantly increase
                number of possible precursors and slow down the predictions. Ignored if confine_to_stables is True.
            simple_precursors (bool or int): If True, or integer >0, precursors with fewer components will be considered.
            explicit_includes (list): list of mp-ids to explicitly include. For example, confine_to_stables may exclude
                certain common precursors in some systems, if they are not on the convex-hull - this allows such
                potential precursors to be added to the library.
            allow_gas_release (bool): Many reactions require the release of gases like CO2, O2, etc. depending on the
                precursors, which requires explicitly considering them in balancing the reactions. Defaults to False.
            add_element (str): Add an element to the chemical space of libraries that doesn't exist in the target
                material. Best example is 'C', which would allow carbonates to be added to the precursor library.
            temperature (float): Temperature (in Kelvin) to consider in free energy adjustments for gases.
            pressure (dict or float): Gas pressures (in atm). If float, all gases are assumed to have the same constant
                pressure. A dictionary in the form of {'O2': 0.21, 'CO2':, 0.05} can be provided to explicitly
                specify partial pressures. If given None, a default pressure dictionary will be used pertaining to
                open atmosphere conditions. Defaults to 1 atm.
            entries (list): List of Materials Project ComputedEntry objects, as can be obtained via the API. If provided
                these entries will be used while forming the precursor library. If not provided, MP database will be
                queried via the Rester API to get the most up-to-date entries. Defaults to None.
            epitaxies (list): List of minimum matching areas between the target and entries, normally as computed
                via the get_epitaxies method. Recommended use is to leave as None.
            similarities: List of similarity quantiles between the target and entries, normally as computed
                via the get_similarities method. Recommended use is to leave as None.
            sigma (float): surface energy constant (eV/Ang^2) to be used in predictions. Defaults to equivalent
                2.0 J/m^2.
            transport_constant (float): diffusion barrier coefficient (max barrier). Defaults to 10.0.
        """

        self.target_entry_id = target_entry_id
        self.confine_to_icsd = confine_to_icsd
        self.confine_to_stables = confine_to_stables
        self.simple_precursors = simple_precursors
        self.explicit_includes = explicit_includes
        self.allow_gas_release = allow_gas_release
        self.temperature = temperature
        self.pressure = pressure if pressure else DEFAULT_GAS_PRESSURES
        self.add_element = add_element
        self.entries = entries
        self.hull_distance = hull_distance

        self._sigma = sigma if sigma else 2 * 6.242 * 0.01
        self._transport_constant = transport_constant if transport_constant else 10.0

        self.plot_data = None
        self.reactions = {}
        if not entries:
            a = MPRester(MP_API_KEY)
            _e = a.get_entry_by_material_id(self.target_entry_id)
            self.elts = list(_e.composition.as_dict().keys())
            if add_element:
                self.elts.append(add_element)
            self.get_mp_entries()
        else:
            self.elts = list(self.target_entry.composition.as_dict().keys())

        self.get_precursor_library()
        self.epitaxies = epitaxies if epitaxies else self.get_epitaxies()
        self.similarities = similarities if similarities else self.get_similarities()
        print("Precursor library ready.")

    def get_mp_entries(self):
        a = MPRester(MP_API_KEY)
        self.entries = a.get_entries_in_chemsys(self.elts, inc_structure='final',
                                                property_data=['icsd_ids', 'formation_energy_per_atom'])

    @property
    def target_entry(self):
        return [e for e in self.entries if e.entry_id == self.target_entry_id][0]

    def get_precursor_library(self):
        phased = PhaseDiagram(self.entries)
        if self.confine_to_stables:
            precursor_library = list(phased.stable_entries)
        elif self.hull_distance < np.inf:
            precursor_library = [e for e in self.entries if phased.get_e_above_hull(e) <= self.hull_distance]
        else:
            precursor_library = self.entries
        if self.confine_to_icsd:
            precursor_library = [i for i in precursor_library if i.data['icsd_ids']]

        if self.simple_precursors:
            precursor_library = [i for i in precursor_library
                                 if len(i.composition.elements) < len(
                    self.target_entry.composition.elements) - self.simple_precursors + 1]

        if self.target_entry in precursor_library:
            precursor_library.pop(precursor_library.index(self.target_entry))

        if self.explicit_includes:
            print("explicitly including: ", self.explicit_includes)
            for entry_id in self.explicit_includes:
                entry = [e for e in self.entries if e.entry_id == entry_id][0]
                if entry not in precursor_library:
                    precursor_library.append(entry)

        self.precursor_library = precursor_library
        return self.precursor_library

    def get_similarities(self):
        _similarities = similarity([s.structure for s in self.precursor_library], self.target_entry.structure)
        self.similarities = dict(zip([i.entry_id for i in self.precursor_library], _similarities))
        print("Similarity matrix ready")
        return self.similarities

    def get_epitaxies(self):
        _epitaxies = epitaxy([s.structure for s in self.precursor_library], self.target_entry.structure)
        self.epitaxies = dict(zip([i.entry_id for i in self.precursor_library], _epitaxies))
        print("Epitaxies ready")
        return self.epitaxies

    def get_reactions(self):

        target_c = get_v(self.target_entry.structure.composition.fractional_composition, self.elts)

        for precursors in itertools.combinations(self.precursor_library, len(self.elts)):

            precursors = list(precursors)

            c = [get_v(e.structure.composition.fractional_composition, self.elts) for e in precursors]
            if np.any(np.sum(np.array(c), axis=0) == 0.0):
                continue

            try:
                coeffs = np.linalg.solve(np.vstack(c).T, target_c)
            except:
                # need better handling here.
                continue

            if np.any(np.abs(coeffs) > 100):
                continue

            precursor_formulas = np.array([p.structure.composition.reduced_formula for p in precursors])

            if np.any(coeffs < 0.0):
                if not self.allow_gas_release:
                    continue
                else:
                    if not set(precursor_formulas[coeffs < 0.0]).issubset(GAS_RELEASE):
                        continue

            for i in sorted(range(len(coeffs)), reverse=True):
                if np.abs(coeffs[i]) < 0.00001:
                    precursors.pop(i)
                    coeffs = np.delete(coeffs, i)

            label = '_'.join(sorted([e.entry_id for e in precursors]))
            if label in self.reactions:
                continue
            else:
                self.reactions[label] = {'precursors': deepcopy(precursors),
                                         'coeffs': coeffs,
                                         'precursor_formulas': np.array([p.structure.composition.reduced_formula
                                                                         for p in precursors]),
                                         'precursor_ids': [p.entry_id for p in precursors]
                                         }
        return self.reactions

    def get_reaction_energy(self, rxn_label):
        precursors = update_gases(self.reactions[rxn_label]['precursors'], T=self.temperature, P=self.pressure,
                                  copy=True)
        energies = np.array([e.data['formation_energy_per_atom'] for e in precursors])
        self.reactions[rxn_label]['energy'] = self.target_entry.data['formation_energy_per_atom'] \
                                              - np.sum(self.reactions[rxn_label]['coeffs'] * energies)
        self.reactions[rxn_label]['temperature'] = self.temperature
        return self.reactions[rxn_label]['energy']

    @staticmethod
    def f(q):
        S = 1. - 2 * q
        if S < -1:
            S = -1
        elif S > 1:
            S = 1
        return (2 - 3 * S + S ** 3) / 4

    @property
    def sigma(self):
        return self._sigma

    @property
    def transport_constant(self):
        return self._transport_constant

    def get_nucleation_barrier(self, rxn_label):
        rx_e = self.reactions[rxn_label]['energy']
        if rx_e > 0.0:
            self.reactions[rxn_label]['barrier'] = np.inf
            self.reactions[rxn_label]['_params'] = None
            return self.reactions[rxn_label]['barrier']

        target_s = self.target_entry.structure
        delta_Gv = rx_e * target_s.num_sites / target_s.volume

        precursors = self.reactions[rxn_label]['precursors']
        precursor_formulas = self.reactions[rxn_label]['precursor_formulas']

        q_epi = min([self.epitaxies[i.entry_id] for i in precursors
                     if not i.structure.composition.reduced_formula in GASES]) / 1000.0
        q_epi = min(q_epi, 1.0)

        try:
            q_sim = min([self.similarities[i.entry_id] for i in precursors
                         if int(
                    self.similarities[i.entry_id]) != -1 and not i.structure.composition.reduced_formula in GASES])
        except:
            # better handling needed
            q_sim = 1.0

        f_t = self.f((q_epi + q_sim) / 2.0)
        G_star = 16 / 3 * np.pi * self.sigma ** 3 * f_t / delta_Gv ** 2
        E_d = self.transport_constant * q_sim

        self.reactions[rxn_label]['barrier'] = G_star + E_d
        self.reactions[rxn_label]['_params'] = {'f_t': f_t, 'G_star': G_star, 'E_d': E_d, 'q_sim': q_sim,
                                                'q_epi': q_epi}

        return self.reactions[rxn_label]['barrier']

    def get_rxn_summary(self, rxn_label):
        coeffs = self.reactions[rxn_label]['coeffs']
        num_sites = sum(self.target_entry.structure.composition.reduced_composition.as_dict().values())
        _coeffs = []
        for i in range(len(coeffs)):
            p = self.reactions[rxn_label]['precursors'][i]
            _coeffs.append(coeffs[i] / sum(p.structure.composition.reduced_composition.as_dict().values()) * num_sites)
        _coeffs = np.round(_coeffs, decimals=4)
        report = ' + '.join(
            [
                i + ' ' + j for i, j in list(
                zip([str(c) for c in _coeffs], [p.structure.composition.reduced_formula + '(' + p.entry_id + ')'
                                                for p in self.reactions[rxn_label]['precursors']]))
            ]
        )
        self.reactions[rxn_label]['summary'] = report
        return report

    def get_competing_phases(self, rxn_label):

        precursors = self.reactions[rxn_label]['precursors']
        precursor_ids = [i.entry_id for i in precursors]
        _competing = []

        for entry in self.entries:
            if not set(self.target_entry.composition.as_dict().keys()).issubset(
                    set(entry.structure.composition.as_dict().keys())):
                continue
            if entry.entry_id in precursor_ids:
                continue
            if entry.entry_id == self.target_entry_id:
                continue
            competing_target_entry = entry

            elts_precs = set()
            for s in [set(p.structure.composition.as_dict().keys()) for p in precursors]:
                elts_precs = elts_precs.union(s)
            elts_precs = sorted(list(elts_precs))

            target_c = get_v(competing_target_entry.structure.composition.fractional_composition, elts_precs)
            c = [get_v(e.structure.composition.fractional_composition, elts_precs) for e in precursors]

            precursor_formulas = np.array([p.structure.composition.reduced_formula for p in precursors])

            # trying to solve for compound fractions.
            try:
                coeffs = np.linalg.solve(np.vstack(c).T, target_c)
            except:
                try:
                    x = scipy.sparse.linalg.lsqr(np.vstack(c).T, target_c)
                    coeffs = x[0]
                    if x[1] != 1:
                        continue
                except:
                    print('failed:', competing_target_entry.composition.reduced_formula, precursor_formulas)
                    print(np.vstack(c).T, target_c)
                    continue

            if np.any(coeffs < 0.0):
                if not self.allow_gas_release:
                    continue
                else:
                    if not set(precursor_formulas[coeffs < 0.0]).issubset(GAS_RELEASE):
                        continue

            precursors = update_gases(precursors, T=self.temperature, copy=True)

            for i in sorted(range(len(coeffs)), reverse=True):
                if np.abs(coeffs[i]) < 0.00001:
                    precursors.pop(i)
                    coeffs = np.delete(coeffs, i)

            energies = np.array([e.data['formation_energy_per_atom'] for e in precursors])
            rx_e = competing_target_entry.data['formation_energy_per_atom'] - np.sum(coeffs * energies)

            if rx_e < 0.0:
                _competing.append(competing_target_entry.entry_id)
        self.reactions[rxn_label]['competing'] = _competing
        self.reactions[rxn_label]['n_competing'] = len(_competing)
        return len(_competing)

    def recommend_routes(self, temperature=298, pressure=None, allow_gas_release=False,
                         max_component_precursors=0, show_fraction_known_precursors=True):
        if not pressure:
            pressure = self.pressure
        if not (
                self.temperature == temperature and self.pressure == pressure and self.allow_gas_release == allow_gas_release
                and self.reactions):
            self.temperature = temperature
            self.pressure = pressure if pressure else self.pressure
            self.allow_gas_release = allow_gas_release
            self.get_reactions()
            for rxn_label in self.reactions:
                self.get_reaction_energy(rxn_label)
                self.get_nucleation_barrier(rxn_label)
                self.get_rxn_summary(rxn_label)
                self.get_competing_phases(rxn_label)
            self.check_if_known_precursors()

        self.plot_data = pd.DataFrame.from_dict(self.reactions, orient='index')[['n_competing', "barrier", "summary",
                                                                                 "exp_precursors"]]
        if max_component_precursors:
            allowed_precursor_ids = [i.entry_id for i in self.precursor_library
                                     if len(set(i.composition.as_dict().keys()).difference(self.add_element))
                                     <= max_component_precursors or i.composition.reduced_formula in GAS_RELEASE]
            display_reactions = []
            for r in self.plot_data.index.to_list():
                if set(r.split('_')).issubset(set(allowed_precursor_ids)):
                    display_reactions.append(r)
            self.plot_data = self.plot_data.loc[display_reactions]

        color = "exp_precursors" if show_fraction_known_precursors else None

        fig = px.scatter(self.plot_data, x="n_competing", y="barrier", hover_data=["summary"],
                             color=color)
        fig.update_layout(
            yaxis={'title': 'Barrier (a.u.)'},
            xaxis={'title': 'N competing phases'},
            title="Synthesis target: " + self.target_entry.structure.composition.reduced_formula)
        fig.show()

    def get_precursor_formulas(self, include_ids=True):
        if include_ids:
            return [(p.entry_id, p.composition.reduced_formula) for p in self.precursor_library]
        else:
            return [p.composition.reduced_formula for p in self.precursor_library]

    def get_rxn_containing(self, formulas):
        """
        Find reactions that contain all formulas given.
        Args:
            formulas: list of formulas. string okay if one formula.
        Returns:
            reaction details
        """
        if isinstance(formulas, str):
            formulas = list(formulas)
        return sorted([(self.reactions[i]['barrier'], self.reactions[i]['summary'], self.reactions[i]['n_competing'])
                for i in self.reactions if all([formula in self.reactions[i]['summary'] for formula in formulas])
                       ])

    def check_if_known_precursors(self):
        with open(os.path.join(RXN_FILES,"experimental_precursors_KononovaSciData.json"), 'r') as f:
            exp_precursors = set(json.load(f))

        for i in self.reactions:
            ids = [self.reactions[i]['precursor_ids'][j] for j in range(len(self.reactions[i]['precursor_ids']))
                   if self.reactions[i]['precursor_formulas'][j] not in GASES]
            frac = len(set(ids).intersection(exp_precursors)) / len(ids)
            self.reactions[i]['exp_precursors'] = str(np.round(frac,decimals=4))

    def get_pareto_front(self):
        """
        Returns: list of reaction labels on the pareto front
        """
        x = self.plot_data.sort_values(by=['n_competing', 'barrier'])[['n_competing', 'barrier']]
        y = x.groupby(by=['n_competing'], as_index=False).min()
        rows = list(y.iterrows())
        front = []
        barrier_front = []
        for row in rows:
            n_competing = row[1]['n_competing']
            barrier = row[1]['barrier']
            if rows.index(row) == 0:
                front.append(x.index[(x['barrier'] == barrier) & (x['n_competing'] == n_competing)][0])
                barrier_front.append(barrier)
                continue
            if barrier < barrier_front[-1]:
                front.append(x.index[(x['barrier'] == barrier) & (x['n_competing'] == n_competing)][0])
                barrier_front.append(barrier)
        return front
