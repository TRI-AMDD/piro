import itertools
from dataclasses import dataclass
from functools import lru_cache

import scipy
from pymatgen.core import Composition
from scipy.special import comb
from typing import List, Tuple, Union

import numpy as np
from pymatgen.entries.computed_entries import ComputedStructureEntry
from tqdm.autonotebook import tqdm

from piro.data import GAS_RELEASE, ST, H, GASES
from piro.utils import get_v, get_ST


@dataclass
class BalancedReaction:
    reduced_formulas: Tuple[str]
    target_entry: ComputedStructureEntry
    coeffs: np.array
    removed_coeff_indexes: List[int]
    main_formulas: List[str]


class SkipReaction(Exception):
    pass


def get_balanced_reaction(
        target_entry: ComputedStructureEntry,
        reduced_formulas: Tuple[str],
        precursors: List[ComputedStructureEntry],
        v_elements_key: str,
        allow_gas_release: bool = False
) -> BalancedReaction:
    if len(set(reduced_formulas)) != len(reduced_formulas):
        raise SkipReaction('Reaction has duplicate formula')

    target_c = target_entry.data[v_elements_key]
    c = np.vstack([p.data[v_elements_key] for p in precursors])

    if not c.sum(axis=0).all():
        raise SkipReaction('Reaction as sum 0 c')

    try:
        coeffs = np.linalg.solve(c.T, target_c)
    except:
        # need better handling here.
        raise SkipReaction('Reaction could not solve for coeffs')

    removed_coeff_indexes = []
    main_formulas = []
    for i, (coeff, reduced_formula) in enumerate(zip(coeffs, reduced_formulas)):
        if abs(coeff) > 100:
            raise SkipReaction('Reaction has a coeff over 100')

        if coeff < 0.0:
            if not allow_gas_release:
                raise SkipReaction('Reaction has a gas release')
            if reduced_formula not in GAS_RELEASE:
                raise SkipReaction('Reaction gas releases are not expected gases')

        if abs(coeff) < 0.0001:
            removed_coeff_indexes.append(i)
        else:
            main_formulas.append(reduced_formula)

    c = np.delete(c, removed_coeff_indexes, 0)
    coeffs = np.delete(coeffs, removed_coeff_indexes)

    effective_rank = scipy.linalg.lstsq(c.T, target_c)[2]
    if effective_rank < len(coeffs):
        # Removes under-determined reactions.
        raise SkipReaction('Reaction is under-determined')

    return BalancedReaction(
        reduced_formulas,
        target_entry,
        coeffs,
        removed_coeff_indexes,
        main_formulas,
    )


class Reaction:

    def __init__(
        self,
        sorted_precursors: List[ComputedStructureEntry],
        balanced_reaction: BalancedReaction
    ):
        self.sorted_precursors = sorted_precursors
        self.balanced_reaction = balanced_reaction

        self.precursors = [
            p for i, p in enumerate(sorted_precursors) if i not in self.balanced_reaction.removed_coeff_indexes
        ]
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
            "coeffs": self.balanced_reaction.coeffs,
            "precursor_formulas": np.array(self.balanced_reaction.main_formulas),
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
        coeffs = self.balanced_reaction.coeffs
        num_sites = self.balanced_reaction.target_entry.data['reduced_composition_sum']
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
                    - get_ST(c, temperature)
                    + 8.6173324e-5 * temperature * np.log(pp) / num_atoms_for_reduced_formula(c)
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
        target_entry_energy = self.balanced_reaction.target_entry.data["formation_energy_per_atom"]
        energies, enthalpies = self.get_energies_and_enthalpies(
            self.precursors,
            temperature,
            pressure
        )
        self.energy = target_entry_energy - np.sum(self.balanced_reaction.coeffs * np.array(energies))
        self.enthalpy = target_entry_energy - np.sum(self.balanced_reaction.coeffs * np.array(enthalpies))
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

        target_s = self.balanced_reaction.target_entry.structure
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

        target_entry_keys = self.balanced_reaction.target_entry.data['composition_keys']

        elts_precs = set()
        for p in self.precursors:
            for k in p.data['composition_keys']:
                elts_precs.add(k)
        sorted_elts_precs = sorted(str(s) for s in elts_precs)
        c = [
            get_v(e.composition.fractional_composition.as_dict(), tuple(sorted_elts_precs))
            for e in self.precursors
        ]

        precursor_formulas = np.array(
            self.balanced_reaction.main_formulas
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
            if entry.entry_id == self.balanced_reaction.target_entry.entry_id:
                continue
            competing_target_entry = entry

            if not entry_keys.issubset(elts_precs):
                # print(entry.composition)
                continue

            if 'fractional_composition_dict' not in competing_target_entry.data:
                competing_target_entry.data['fractional_composition_dict'] = \
                    competing_target_entry.composition.fractional_composition.as_dict()

            target_c = get_v(
                competing_target_entry.data['fractional_composition_dict'],
                tuple(sorted_elts_precs),
            )

            # trying to solve for compound fractions.
            np_vstack_c__t = np.vstack(c).T
            try:
                coeffs = np.linalg.solve(np_vstack_c__t, target_c)
            except:
                try:
                    x = scipy.sparse.linalg.lsqr(np_vstack_c__t, target_c)
                    coeffs = x[0]
                    if x[1] != 1:
                        continue
                except:
                    print(
                        "     failed:",
                        competing_target_entry.composition.reduced_formula,
                        precursor_formulas,
                    )
                    print(np_vstack_c__t, target_c)
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
                effective_rank = scipy.linalg.lstsq(np_vstack_c__t, target_c)[2]
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


def get_reactions(
    target_entry: ComputedStructureEntry,
    elements: List[str],
    precursor_library: List[ComputedStructureEntry],
    allow_gas_release: bool = False,
) -> List[Reaction]:

    v_elements_key = f'v_{"_".join(elements)}'
    cache_common_calculations(target_entry, tuple(elements), precursor_library, v_elements_key)
    balanced_reaction_by_reduced_formulas = dict()
    skipped = set()

    reactions = []

    for sorted_precursors in tqdm(
        itertools.combinations(sorted(precursor_library, key=lambda p: p.data['reduced_formula']), len(elements)),
        desc="balancing reactions",
        total=comb(len(precursor_library), len(elements)),
    ):
        reduced_formulas = tuple([str(p.data['reduced_formula']) for p in sorted_precursors])

        if reduced_formulas in skipped:
            continue

        if reduced_formulas not in balanced_reaction_by_reduced_formulas:
            try:
                balanced_reaction = get_balanced_reaction(
                    target_entry,
                    reduced_formulas,
                    sorted_precursors,
                    v_elements_key,
                    allow_gas_release
                )
            except SkipReaction:
                skipped.add(reduced_formulas)
                continue
            balanced_reaction_by_reduced_formulas[reduced_formulas] = balanced_reaction

        balanced_reaction = balanced_reaction_by_reduced_formulas[reduced_formulas]
        reaction = Reaction(sorted_precursors, balanced_reaction)
        reactions.append(reaction)

    return reactions


def cache_common_calculations(
    target_entry: ComputedStructureEntry,
    elements: Tuple[str],
    precursor_library: List[ComputedStructureEntry],
    v_elements_key: str
):
    target_entry.data[v_elements_key] = get_v(target_entry.composition.fractional_composition.as_dict(), elements)
    target_entry.data['composition_keys'] = set(target_entry.composition.as_dict().keys())
    target_entry.data['reduced_composition_sum'] = sum(target_entry.composition.reduced_composition.as_dict().values())

    for p in precursor_library:
        p.data[v_elements_key] = get_v(p.composition.fractional_composition.as_dict(), elements)
        p.data['reduced_formula'] = p.composition.reduced_formula
        p.data['composition_keys'] = set(p.composition.as_dict().keys())
        p.data['reduced_composition_sum'] = sum(p.composition.reduced_composition.as_dict().values())


@lru_cache()
def num_atoms_for_reduced_formula(c):
    return Composition(c).num_atoms
