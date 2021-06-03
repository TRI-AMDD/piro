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
from pymatgen.util.string import latexify
from piro.data import GASES, GAS_RELEASE, DEFAULT_GAS_PRESSURES
from piro.utils import get_v, epitaxy, similarity, update_gases, through_cache
from piro import MP_API_KEY, RXN_FILES
from tqdm.autonotebook import tqdm
from scipy.special import comb


# TODO: for elements and gases (references) - don't allow multiple entries
# TODO: for E_d, test q = max(q_phases) - max of q, assuming that would be the limiting step


class SynthesisRoutes:
    def __init__(self, target_entry_id, confine_to_icsd=True, confine_to_stables=True, hull_distance=np.inf,
                 simple_precursors=False, explicit_includes=None, allow_gas_release=False,
                 add_element=None, temperature=298, pressure=1, use_cache=True, exclude_compositions=None,
                 entries=None, epitaxies=None, similarities=None, sigma=None, transport_constant=None,
                 custom_target_entry=None, flexible_competition=None):
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
            exclude_compositions (list): list of compositions to avoid in precursor library.
            allow_gas_release (bool): Many reactions require the release of gases like CO2, O2, etc. depending on the
                precursors, which requires explicitly considering them in balancing the reactions. Defaults to False.
            add_element (str): Add an element to the chemical space of libraries that doesn't exist in the target
                material. Best example is 'C', which would allow carbonates to be added to the precursor library.
            temperature (float): Temperature (in Kelvin) to consider in free energy adjustments for gases.
            pressure (dict or float): Gas pressures (in atm). If float, all gases are assumed to have the same constant
                pressure. A dictionary in the form of {'O2': 0.21, 'CO2':, 0.05} can be provided to explicitly
                specify partial pressures. If given None, a default pressure dictionary will be used pertaining to
                open atmosphere conditions. Defaults to 1 atm.
            use_cache (bool): if True, caches the epitaxy and similarity information for future reuse.
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
            custom_target_entry (MP entry): custom computed entry object pymatgen
            flexible_competition (int): whether lower order targets are allowed in competing reactions. Defaults to 0
                which forces competing reactions to have products of the same order as target. If 1, one order smaller
                compounds and so on.
        """

        self.target_entry_id = target_entry_id
        self.confine_to_icsd = confine_to_icsd
        self.confine_to_stables = confine_to_stables
        self.simple_precursors = simple_precursors
        self.explicit_includes = explicit_includes if explicit_includes else []
        self.allow_gas_release = allow_gas_release
        self.temperature = temperature
        self.pressure = pressure if pressure else DEFAULT_GAS_PRESSURES
        self.add_element = add_element if add_element else []
        self.entries = entries
        self.hull_distance = hull_distance
        self.use_cache = use_cache
        self.confine_competing_to_icsd = False
        self.exclude_compositions = exclude_compositions
        self.custom_target_entry = custom_target_entry
        self.flexible_competition = flexible_competition if flexible_competition else 0
        self._sigma = sigma if sigma else 2 * 6.242 * 0.01
        self._transport_constant = transport_constant if transport_constant else 10.0

        self.plot_data = None
        self.reactions = {}
        if not entries:
            a = MPRester(MP_API_KEY)
            if not custom_target_entry:
                _e = a.get_entry_by_material_id(self.target_entry_id)
            else:
                _e = custom_target_entry
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
        for entry in self.entries:
            entry.structure.entry_id = entry.entry_id
        print('Total # of entries found in this chemistry: ', len(self.entries))

    @property
    def target_entry(self):
        if self.custom_target_entry:
            return self.custom_target_entry
        else:
            return [e for e in self.entries if e.entry_id == self.target_entry_id][0]

    def get_precursor_library(self):
        phased = PhaseDiagram(self.entries)
        if self.confine_to_stables:
            precursor_library = list(phased.stable_entries)
        elif self.hull_distance < np.inf:
            precursor_library = [e for e in self.entries if phased.get_e_above_hull(e) <= self.hull_distance]
        else:
            precursor_library = [e for e in self.entries]
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
                try:
                    entry = [e for e in self.entries if e.entry_id == entry_id][0]
                except:
                    print("Could not find {} in entry list".format(entry_id))
                    continue
                if entry not in precursor_library:
                    precursor_library.append(entry)

        if self.exclude_compositions:
            precursor_library = [i for i in precursor_library if i.composition.reduced_formula
                                 not in self.exclude_compositions]

        self.precursor_library = precursor_library

        print('Total # of precusors materials obeying the provided filters: ',len(precursor_library))
        return self.precursor_library

    def get_similarities(self):
        if self.use_cache:
            _similarities = through_cache([s.structure for s in self.precursor_library],
                                          self.target_entry.structure, type="similarity")
        else:
            _similarities = similarity([s.structure for s in self.precursor_library], self.target_entry.structure)
        self.similarities = dict(zip([i.entry_id for i in self.precursor_library], _similarities))
        print("Similarity matrix ready")
        return self.similarities

    def get_epitaxies(self):
        if self.use_cache:
            _epitaxies = through_cache([s.structure for s in self.precursor_library],
                                       self.target_entry.structure, type="epitaxy")
        else:
            _epitaxies = epitaxy([s.structure for s in self.precursor_library], self.target_entry.structure)
        self.epitaxies = dict(zip([i.entry_id for i in self.precursor_library], _epitaxies))
        print("Epitaxies ready")
        return self.epitaxies

    def get_reactions(self):

        target_c = get_v(self.target_entry.structure.composition.fractional_composition, self.elts)

        for precursors in tqdm(itertools.combinations(self.precursor_library, len(self.elts)),
                               total=comb(len(self.precursor_library),len(self.elts))):

            precursors = list(precursors)

            c = [get_v(e.structure.composition.fractional_composition, self.elts) for e in precursors]
            if np.any(np.sum(np.array(c), axis=0) == 0.0):
                continue

            try:
                coeffs = np.linalg.solve(np.vstack(c).T, target_c)
                effective_rank = scipy.linalg.lstsq(np.vstack(c).T, target_c)[2]
            except:
                # need better handling here.
                continue

            if np.any(np.abs(coeffs) > 100):
                continue

            precursor_formulas = np.array([p.structure.composition.reduced_formula for p in precursors])
            if len(set(precursor_formulas)) != len(precursor_formulas):
                continue

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
                    # Update effective rank
                    c_new = [get_v(e.structure.composition.fractional_composition, self.elts) for e in precursors]
                    effective_rank = scipy.linalg.lstsq(np.vstack(c_new).T, target_c)[2]
            if effective_rank<len(coeffs):
                # Removes under-determined reactions.
                # print(effective_rank, precursor_formulas, \
                # [prec_.composition.reduced_formula for prec_ in precursors],coeffs)
                continue

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
        print("Total # of balanced reactions obtained: ", len(self.reactions))
        return self.reactions

    def get_reaction_energy(self, rxn_label, verbose=False):
        precursors = update_gases(self.reactions[rxn_label]['precursors'], T=self.temperature, P=self.pressure,
                                  copy=True)
        # Free energy per atom
        energies = np.array([e.data['formation_energy_per_atom'] for e in precursors])
        self.reactions[rxn_label]['energy'] = self.target_entry.data['formation_energy_per_atom'] \
                                              - np.sum(self.reactions[rxn_label]['coeffs'] * energies)
        # Enthalpy energy per atom
        enthalpies = np.array([e.data['enthalpy'] if 'enthalpy' in e.data
                               else e.data['formation_energy_per_atom'] for e in precursors])
        self.reactions[rxn_label]['enthalpy'] = self.target_entry.data['formation_energy_per_atom'] \
                                              - np.sum(self.reactions[rxn_label]['coeffs'] * enthalpies)

        self.reactions[rxn_label]['temperature'] = self.temperature

        if verbose:
            print('target e: ', self.target_entry.data['formation_energy_per_atom'])
            print('precursr: ', [e.composition.reduced_formula for e in precursors])
            print('energies: ', energies)
            print('coeffs:   ', self.reactions[rxn_label]['coeffs'])

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

    def get_competing_phases(self, rxn_label, confine_to_icsd=True):

        precursors = self.reactions[rxn_label]['precursors']
        precursor_ids = [i.entry_id for i in precursors]
        _competing = []
        _competing_rxe = []

        for entry in self.entries:
            if confine_to_icsd:
                if not entry.data['icsd_ids']:
                    continue
            if self.flexible_competition:
                s1 = set(entry.composition.as_dict().keys())
                s2 = set(self.target_entry.structure.composition.as_dict().keys())
                if not (s1.issubset(s2)
                        and (len(s2)-self.flexible_competition <= len(s1) <= len(s2))
                        ):
                    continue
            else:
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
            if not set(entry.composition.as_dict().keys()).issubset(elts_precs):
                # print(entry.composition)
                continue

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
                    print('     failed:', competing_target_entry.composition.reduced_formula, precursor_formulas)
                    print(np.vstack(c).T, target_c)
                    continue
            if np.any(coeffs < 0.0):
                if not self.allow_gas_release:
                    continue
                else:
                    if not set(precursor_formulas[coeffs < 0.0]).issubset(GAS_RELEASE):
                        continue
            _precursors = update_gases(precursors, T=self.temperature, P=self.pressure, copy=True)

            for i in sorted(range(len(coeffs)), reverse=True):
                if np.abs(coeffs[i]) < 0.00001:
                    _precursors.pop(i)
                    coeffs = np.delete(coeffs, i)

            try:
                effective_rank = scipy.linalg.lstsq(np.vstack(c).T, target_c)[2]
                if effective_rank < len(coeffs):
                    # print(precursor_formulas, coeffs)
                    # Removes under-determined reactions.
                    continue
            except:
                continue
            energies = np.array([e.data['formation_energy_per_atom'] for e in _precursors])
            rx_e = competing_target_entry.data['formation_energy_per_atom'] - np.sum(coeffs * energies)
            if rx_e < 0.0:
                _competing.append(competing_target_entry.entry_id)
                _competing_rxe.append((rx_e))
        self.reactions[rxn_label]['competing'] = _competing
        self.reactions[rxn_label]['competing_rxe'] = _competing_rxe
        self.reactions[rxn_label]['n_competing'] = len(_competing)
        return len(_competing)

    def recommend_routes(self, temperature=298, pressure=None, allow_gas_release=False,
                         max_component_precursors=0, show_fraction_known_precursors=True,
                         show_known_precursors_only=False, confine_competing_to_icsd=True,
                         display_peroxides=True, display_superoxides=True, w=None, h=None,
                         xrange=None, yrange=None, add_pareto=False, custom_text=''):
        if not pressure:
            pressure = self.pressure
        if not (
                self.temperature == temperature and self.pressure == pressure and
                self.allow_gas_release == allow_gas_release and
                self.confine_competing_to_icsd == confine_competing_to_icsd and
                self.reactions):
            self.temperature = temperature
            self.pressure = pressure if pressure else self.pressure
            self.allow_gas_release = allow_gas_release
            self.confine_competing_to_icsd = confine_competing_to_icsd
            self.get_reactions()
            for rxn_label in self.reactions:
                self.get_reaction_energy(rxn_label)
                self.get_nucleation_barrier(rxn_label)
                self.get_rxn_summary(rxn_label)
                self.get_competing_phases(rxn_label, confine_to_icsd=confine_competing_to_icsd)
            self.check_if_known_precursors()

        self.plot_data = pd.DataFrame.from_dict(self.reactions, orient='index')[['n_competing', "barrier", "summary",
                                                                                 "energy", "enthalpy",
                                                                                 "exp_precursors", "precursor_formulas"]]
        if max_component_precursors:
            allowed_precursor_ids = [i.entry_id for i in self.precursor_library
                                     if len(set(i.composition.as_dict().keys()).difference(self.add_element))
                                     <= max_component_precursors or i.composition.reduced_formula in GAS_RELEASE]
            display_reactions = []
            for r in self.plot_data.index.to_list():
                if set(r.split('_')).issubset(set(allowed_precursor_ids)):
                    display_reactions.append(r)
            self.plot_data = self.plot_data.loc[display_reactions]

        if not display_peroxides:
            peroxides = {'Li2O2', 'K2O2', 'BaO2', 'Rb2O2', 'Cs2O2', 'Na2O2', 'SrO2',
                         'CaO2','MgO2', 'ZnO2', 'CdO2', 'HgO2'}
            allowed_rows = []
            for i in range(len(self.plot_data)):
                if not peroxides.intersection(set(self.plot_data["precursor_formulas"][i].tolist())):
                    allowed_rows.append((i))
            self.plot_data = self.plot_data.iloc[allowed_rows]

        if not display_superoxides:
            superoxides = {'LiO2', 'NaO2', 'KO2', 'RbO2', 'CsO2'}
            allowed_rows = []
            for i in range(len(self.plot_data)):
                if not superoxides.intersection(set(self.plot_data["precursor_formulas"][i].tolist())):
                    allowed_rows.append((i))
            self.plot_data = self.plot_data.iloc[allowed_rows]

        color = "exp_precursors" if show_fraction_known_precursors else None

        if show_known_precursors_only:
            self.plot_data = self.plot_data[ self.plot_data["exp_precursors"].astype(float) == 1.0 ]
        fig = px.scatter(self.plot_data, x="n_competing", y="barrier", hover_data=["summary"],
                             color=color, width=w, height=h, template='simple_white')
        for i in fig.data:
            i.marker.size = 10
        fig.update_layout(
            yaxis={'title': 'Nucleation barrier (a.u.)', 'ticks': 'inside', 'mirror': True, 'showline': True},
            xaxis={'title': 'Number of competing phases', 'ticks': 'inside', 'mirror': True, 'showline': True},
            font={'size': 13},
            title=r"Target: " + self.target_entry.structure.composition.reduced_formula + custom_text,
            title_font_size=15,
            title_x=0.5)
        fig.update_traces(
            marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey'), opacity=0.8),  selector=dict(mode='markers')
        )
        if xrange:
            fig.update_xaxes(range=xrange)
        if yrange:
            fig.update_yaxes(range=yrange)

        if add_pareto:
            import plotly.graph_objects as go
            _pareto_data = self.topsis().loc[self.get_pareto_front()]
            _x = _pareto_data['n_competing']
            _y = _pareto_data['barrier']
            fig.add_trace(go.Scatter(
                x=_x,
                y=_y,
                line=dict(color='firebrick', width=2)
                # connectgaps=True
            ))
            fig.add_trace(go.Scatter(
                x=[_x[0], _x[0], None, _x[-1], self.topsis()['n_competing'].max()],
                y=[_y[0], self.topsis()['barrier'].max(), None, _y[-1],_y[-1]],
                line=dict(color='firebrick', width=2, dash='dash'),
                connectgaps=False
            ))

            fig.update_layout(showlegend=False)
        return fig

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
        return sorted([(self.reactions[i]['barrier'], self.reactions[i]['summary'], self.reactions[i]['n_competing'],i)
                for i in self.reactions if all([formula in self.reactions[i]['summary'] for formula in formulas])
                       ])

    def check_if_known_precursors(self):
        with open(os.path.join(RXN_FILES,"experimental_precursors_KononovaSciData.json"), 'r') as f:
            exp_precursors = set(json.load(f))
        exp_precursors = exp_precursors.union(set(self.explicit_includes))

        for i in self.reactions:
            ids = [self.reactions[i]['precursor_ids'][j] for j in range(len(self.reactions[i]['precursor_ids']))
                   if self.reactions[i]['precursor_formulas'][j] not in GASES]
            frac = len(set(ids).intersection(exp_precursors)) / len(ids)
            self.reactions[i]['exp_precursors'] = str(np.round(frac,decimals=4))

    def get_pareto_front(self):
        """
        Returns: list of reaction labels on the pareto front
        """
        x = self.plot_data[self.plot_data['barrier'] < np.inf].sort_values(by=['n_competing',
                                                                               'barrier'])[['n_competing', 'barrier']]
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

    def topsis(self, latex=False):
        """
        Returns a ranked list of reactions based on TOPSIS method for multiobjective optimization.
        Returns:
        """
        x = self.plot_data[['n_competing','barrier']]
        x = x[x['barrier'] < np.inf]
        xsum = np.sqrt((x ** 2).sum())
        mu = x / xsum
        positive_ideal = mu.min()
        negative_ideal = mu.max()
        d_pos_ideal = np.sqrt(((mu - positive_ideal) ** 2).sum(axis=1))
        d_neg_ideal = np.sqrt(((mu - negative_ideal) ** 2).sum(axis=1))
        x['topsis_score'] = d_neg_ideal / (d_pos_ideal + d_neg_ideal)
        x = x.sort_values(by='topsis_score', ascending=False)
        result = self.plot_data.loc[x.index]
        result['topsis_score'] = x['topsis_score']

        if latex:
            result['summary'] = result['summary'].apply(latexify)
        return result
