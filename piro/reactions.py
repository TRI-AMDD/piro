import itertools
import logging
import scipy
from numpy import ndarray
from pymatgen.core import Composition
from scipy.special import comb
from typing import List, Dict, Tuple, Any, Union

import numpy as np
from pymatgen.entries.computed_entries import ComputedStructureEntry
from tqdm.autonotebook import tqdm

from piro.data import GAS_RELEASE, ST, H, GASES
from piro.utils import get_v

logger = logging.getLogger(__name__)


class Reaction:

    class SkipReaction(Exception):
        pass

    def __init__(
            self,
            reduced_formulas: Tuple[str],
            target_entry: ComputedStructureEntry,
            elements: List[str]
    ):
        self.reduced_formulas = reduced_formulas

        self.elements = elements
        self.target_entry = target_entry

        self.coeffs = None
        self.removed_coeff_indexes = []
        self.main_formulas = None

    def get_balanced_reaction(
            self,
            precursors: List[ComputedStructureEntry],
            allow_gas_release: bool = False
    ) -> Tuple[Any, List[int], ndarray]:
        if len(set(self.reduced_formulas)) != len(self.reduced_formulas):
            raise self.SkipReaction('Reaction has duplicate formula')

        target_c = self.target_entry.data['v']
        c = np.vstack([p.data['v'] for p in precursors])

        if np.any(np.sum(c, axis=0) == 0.0):
            raise self.SkipReaction('Reaction as sum 0 c')

        try:
            coeffs = np.linalg.solve(c.T, target_c)
        except:
            # need better handling here.
            raise self.SkipReaction('Reaction could not solve for coeffs')

        if np.any(np.abs(coeffs) > 100):
            raise self.SkipReaction('Reaction has a coeff over 100')

        if np.any(coeffs < 0.0):
            if not allow_gas_release:
                raise self.SkipReaction('Reaction has a gas release')
            else:
                if not set(np.array(self.reduced_formulas)[coeffs < 0.0]).issubset(GAS_RELEASE):
                    raise self.SkipReaction('Reaction gas releases are not expected gases')

        removed_coeff_indexes = []
        for i in reversed(range(len(coeffs))):
            if np.abs(coeffs[i]) < 0.00001:
                c = np.delete(c, i, 0)
                coeffs = np.delete(coeffs, i)
                removed_coeff_indexes.append(i)

        effective_rank = scipy.linalg.lstsq(c.T, target_c)[2]
        if effective_rank < len(coeffs):
            # Removes under-determined reactions.
            # print(effective_rank, precursor_formulas, \
            # [prec_.composition.reduced_formula for prec_ in precursors],coeffs)
            raise self.SkipReaction('Reaction is under-determined')

        main_formulas = np.array([
            p for i, p in enumerate(self.reduced_formulas) if i not in removed_coeff_indexes
        ])

        self.coeffs = coeffs
        self.removed_coeff_indexes = removed_coeff_indexes
        self.main_formulas = main_formulas
        return self.coeffs, self.removed_coeff_indexes, self.main_formulas

    def filter_entries(self, entries: List[ComputedStructureEntry]) -> List[ComputedStructureEntry]:
        return [e for i, e in enumerate(entries) if i not in self.removed_coeff_indexes]


class ReactionResult:

    def __init__(
        self,
        sorted_precursors: List[ComputedStructureEntry],
        reaction: Reaction
    ):
        self.sorted_precursors = sorted_precursors
        self.reaction = reaction

        self.precursors = self.reaction.filter_entries(sorted_precursors)
        self.entry_ids = [str(p.entry_id) for p in self.precursors]
        self.label = "_".join(sorted(self.entry_ids))

        self.energy = None
        self.enthalpy = None
        self.temperature = None

        self.barrier = None
        self._params = None

        self.summary = None

        self.competing = None
        self.competing_rxe = None
        self.n_competing = None

    def as_dict(self) -> dict:
        return {
            "precursors": self.precursors,
            "coeffs": self.reaction.coeffs,
            "precursor_formulas": self.reaction.main_formulas,
            "precursor_ids": self.entry_ids,
            "energy": self.energy,
            "enthalpy": self.enthalpy,
            "temperature": self.temperature,
            "barrier": self.barrier,
            "_params": self._params,
            "summary": self.summary,
            "competing": self.competing,
            "competing_rxe": self.competing_rxe,
            "n_competing": self.n_competing
        }

    def update_reaction_summary(self):
        coeffs = self.reaction.coeffs
        num_sites = self.reaction.target_entry.data['reduced_composition_sum']
        _coeffs = []
        for i in range(len(coeffs)):
            p = self.precursors[i]
            _coeffs.append(
                coeffs[i]
                / p.data['reduced_composition_sum']
                * num_sites
            )
        _coeffs = np.round(_coeffs, decimals=4)
        report = " + ".join(
            [f'{str(c)} {p.data["reduced_formula"]}({str(p.entry_id)})' for c, p in zip(_coeffs, self.precursors)]
        )
        self.summary = report
        return self.summary

    @staticmethod
    def get_energies_and_enthalpies(
            entries: List[ComputedStructureEntry],
            temperature: float,
            pressure: Union[float, dict] = 1
    ) -> Tuple[List[float], List[float]]:
        """
        Modify entry objects corresponding to gas phases to account for enthalpy and entropy
        changes wrt. T and standard pressure.
        """
        formation_energy_per_atom_list = []
        enthalpy_list = []
        for e in entries:
            c = e.data['reduced_formula']
            if c in ST:
                if isinstance(pressure, dict):
                    pp = pressure.get(c, 1.0)
                else:
                    pp = pressure
                formation_energy_per_atom_list.append(
                    H.get(c, 0.0)
                    - ST[c][temperature]
                    + 8.6173324e-5 * temperature * np.log(pp) / Composition(c).num_atoms
                )
                enthalpy_list.append(H.get(c, 0.0))
            else:
                formation_energy_per_atom_list.append(e.data['formation_energy_per_atom'])
                enthalpy_list.append(
                    e.data['enthalpy'] if 'enthalpy' in e.data else e.data['formation_energy_per_atom']
                )

        return formation_energy_per_atom_list, enthalpy_list

    def update_reaction_energy(
            self,
            temperature: float = 298,
            pressure: Union[float, dict] = 1
    ) -> float:
        target_entry_energy = self.reaction.target_entry.data["formation_energy_per_atom"]
        energies, enthalpies = self.get_energies_and_enthalpies(
            self.precursors,
            temperature,
            pressure
        )
        self.energy = target_entry_energy - np.sum(self.reaction.coeffs * np.array(energies))
        self.enthalpy = target_entry_energy - np.sum(self.reaction.coeffs * np.array(enthalpies))
        self.temperature = temperature

        return self.energy

    @staticmethod
    def f(q):
        S = 1.0 - 2 * q
        if S < -1:
            S = -1
        elif S > 1:
            S = 1
        return (2 - 3 * S + S ** 3) / 4

    def update_nucleation_barrier(
            self,
            epitaxies: dict,
            similarities: dict,
            sigma: float,
            transport_constant: float
    ) -> float:
        if self.energy > 0.0:
            self.barrier = np.inf
            self._params = None
            return self.barrier

        target_s = self.reaction.target_entry.structure
        delta_Gv = self.energy * target_s.num_sites / target_s.volume

        q_epi = (
            min(
                [
                    epitaxies[i.entry_id]
                    for i in self.precursors
                    if i.data['reduced_formula'] not in GASES
                ]
            )
            / 1000.0
        )
        q_epi = min(q_epi, 1.0)

        try:
            q_sim = min(
                [
                    similarities[i.entry_id]
                    for i in self.precursors
                    if int(similarities[i.entry_id]) != -1
                    and i.data['reduced_formula'] not in GASES
                ]
            )
        except:
            # better handling needed
            q_sim = 1.0

        f_t = self.f((q_epi + q_sim) / 2.0)
        G_star = 16 / 3 * np.pi * sigma ** 3 * f_t / delta_Gv ** 2
        E_d = transport_constant * q_sim

        self.barrier = G_star + E_d
        self._params = {
            "f_t": f_t,
            "G_star": G_star,
            "E_d": E_d,
            "q_sim": q_sim,
            "q_epi": q_epi,
        }

        return self.barrier

    def update_competing_phases(
            self,
            entries: List[ComputedStructureEntry],
            confine_to_icsd: bool = True,
            flexible_competition: int = 0,
            allow_gas_release: bool = False,
            temperature: float = 298,
            pressure: Union[float, dict] = 1

    ):

        precursor_ids = [i.entry_id for i in self.precursors]
        _competing = []
        _competing_rxe = []

        target_entry_keys = self.reaction.target_entry.data['composition_keys']

        elts_precs = set()
        for p in self.precursors:
            for k in p.data['composition_keys']:
                elts_precs.add(k)
        sorted_elts_precs = sorted(str(s) for s in elts_precs)
        c = [
            get_v(e.composition.fractional_composition, tuple(sorted_elts_precs))
            for e in self.precursors
        ]

        precursor_formulas = np.array(
            self.reaction.main_formulas
        )

        for entry in entries:
            if confine_to_icsd:
                if not entry.data["icsd_ids"]:
                    continue

            if 'composition_keys' not in entry.data:
                entry.data['composition_keys'] = set(entry.composition.as_dict().keys())

            entry_keys = entry.data['composition_keys']
            if flexible_competition:
                if not (
                    entry_keys.issubset(target_entry_keys)
                    and
                    (len(target_entry_keys) - flexible_competition <= len(entry_keys) <= len(target_entry_keys))
                ):
                    continue
            else:
                if not target_entry_keys.issubset(entry_keys):
                    continue
            if entry.entry_id in precursor_ids:
                continue
            if entry.entry_id == self.reaction.target_entry.entry_id:
                continue
            competing_target_entry = entry

            if not entry_keys.issubset(elts_precs):
                # print(entry.composition)
                continue

            target_c = get_v(
                competing_target_entry.composition.fractional_composition,
                tuple(sorted_elts_precs),
            )

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
                    print(
                        "     failed:",
                        competing_target_entry.composition.reduced_formula,
                        precursor_formulas,
                    )
                    print(np.vstack(c).T, target_c)
                    continue
            if np.any(coeffs < 0.0):
                if not allow_gas_release:
                    continue
                else:
                    if not set(precursor_formulas[coeffs < 0.0]).issubset(GAS_RELEASE):
                        continue

            indexes_to_remove = []
            for i in sorted(range(len(coeffs)), reverse=True):
                if np.abs(coeffs[i]) < 0.00001:
                    indexes_to_remove.append(i)
                    coeffs = np.delete(coeffs, i)

            try:
                effective_rank = scipy.linalg.lstsq(np.vstack(c).T, target_c)[2]
                if effective_rank < len(coeffs):
                    # print(precursor_formulas, coeffs)
                    # Removes under-determined reactions.
                    continue
            except:
                continue

            energies, _ = self.get_energies_and_enthalpies(
                [p for i, p in enumerate(self.precursors) if i not in indexes_to_remove],
                temperature,
                pressure
            )

            rx_e = competing_target_entry.data["formation_energy_per_atom"] - np.sum(
                coeffs * energies
            )
            if rx_e < 0.0:
                _competing.append(competing_target_entry.entry_id)
                _competing_rxe.append((rx_e))
        self.competing = _competing
        self.competing_rxe = _competing_rxe
        self.n_competing = len(_competing)
        return self.n_competing


class Reactions:

    def __init__(
            self,
            target_entry: ComputedStructureEntry,
            elements: List[str],
            precursor_library: List[ComputedStructureEntry],
            epitaxies: dict,
            similarities: dict,
            entries: List[ComputedStructureEntry],
            allow_gas_release: bool = False,
            temperature: float = 298,
            pressure: Union[float, dict] = 1,
            sigma: float = 2 * 6.242 * 0.01,
            transport_constant: float = 10.0,
            confine_competing_to_icsd: bool = True,
            flexible_competition: int = 0
    ):
        self.target_entry = target_entry
        self.elements = elements
        self.precursor_library = precursor_library
        self.allow_gas_release = allow_gas_release

        self.temperature = temperature
        self.pressure = pressure

        self.epitaxies = epitaxies
        self.similarities = similarities
        self.sigma = sigma
        self.transport_constant = transport_constant

        self.entries = entries
        self.confine_competing_to_icsd = confine_competing_to_icsd
        self.flexible_competition = flexible_competition

    def get_reactions(self) -> Dict:
        self.cache_common_calculations()

        reactions_dict = {}
        reaction_by_reduced_formulas = dict()

        for precursors in tqdm(
                itertools.combinations(self.precursor_library, len(self.elements)),
                total=comb(len(self.precursor_library), len(self.elements)),
        ):
            sorted_precursors = sorted(precursors, key=lambda p: p.data['reduced_formula'])
            reduced_formulas = tuple([str(p.data['reduced_formula']) for p in sorted_precursors])

            if reduced_formulas not in reaction_by_reduced_formulas:
                reaction = Reaction(reduced_formulas, self.target_entry, self.elements)
                try:
                    reaction.get_balanced_reaction(sorted_precursors, self.allow_gas_release)
                except Reaction.SkipReaction as e:
                    logger.debug("Skipping precursors %s: %s", precursors, e)
                    continue
                reaction_by_reduced_formulas[reduced_formulas] = reaction

            reaction = reaction_by_reduced_formulas[reduced_formulas]
            reaction_result = ReactionResult(sorted_precursors, reaction)

            if reaction_result.label in reactions_dict:
                continue
            else:
                reaction_result.update_reaction_energy(
                    self.temperature,
                    self.pressure
                )
                reaction_result.update_nucleation_barrier(
                    self.epitaxies,
                    self.similarities,
                    self.sigma,
                    self.transport_constant
                )
                reaction_result.update_reaction_summary()
                reaction_result.update_competing_phases(
                    self.entries,
                    self.confine_competing_to_icsd,
                    self.flexible_competition,
                    self.allow_gas_release,
                    self.temperature,
                    self.pressure
                )
                reactions_dict[reaction_result.label] = reaction_result.as_dict()

        logger.info(f"Total # of balanced reactions obtained: {len(reactions_dict)}")
        return reactions_dict

    def cache_common_calculations(self):
        self.target_entry.data['v'] = get_v(
            self.target_entry.composition.fractional_composition, tuple(self.elements)
        )
        self.target_entry.data['composition_keys'] = set(self.target_entry.composition.as_dict().keys())
        self.target_entry.data['reduced_composition_sum'] = sum(
            self.target_entry.composition.reduced_composition.as_dict().values()
        )
        for p in self.precursor_library:
            p.data['v'] = get_v(
                p.composition.fractional_composition, tuple(self.elements)
            )
            p.data['reduced_formula'] = p.composition.reduced_formula
            p.data['composition_keys'] = set(p.composition.as_dict().keys())
            p.data['reduced_composition_sum'] = sum(p.composition.reduced_composition.as_dict().values())
