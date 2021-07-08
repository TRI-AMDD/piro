import itertools
import logging
from copy import deepcopy

import scipy
from numpy import ndarray
from scipy.special import comb
from typing import List, Dict, Tuple, Any

import numpy as np
from pymatgen.entries.computed_entries import ComputedStructureEntry
from tqdm.autonotebook import tqdm

from piro.data import GAS_RELEASE
from piro.utils import get_fractional_composition, get_v, get_reduced_formula


logger = logging.getLogger(__name__)


class Reaction:

    class SkipReaction(Exception):
        pass

    def __init__(
            self,
            precursors: List[ComputedStructureEntry],
            target_entry: ComputedStructureEntry,
            elements: List[str],
            allow_gas_release: bool = False
    ):
        self.precursors = precursors
        self.reduced_formulas = tuple([get_reduced_formula(p) for p in self.precursors])

        if len(set(self.reduced_formulas)) != len(self.reduced_formulas):
            raise self.SkipReaction(f'Reaction has duplicate formula')

        self.elements = elements
        self.allow_gas_release = allow_gas_release
        self.target_entry = target_entry

        self.coeffs = None
        self.removed_coeff_indexes = None
        self.main_formulas = None

    def get_balanced_reaction(self) -> Tuple[Any, List[int], ndarray]:
        target_c = get_v(
            get_fractional_composition(self.target_entry), self.elements
        )

        c = [
            get_v(e, self.elements)
            for e in [get_fractional_composition(p) for p in self.precursors]
        ]
        if np.any(np.sum(np.array(c), axis=0) == 0.0):
            raise self.SkipReaction(f'Reaction as sum 0 c')

        try:
            coeffs = np.linalg.solve(np.vstack(c).T, target_c)
        except:
            # need better handling here.
            raise self.SkipReaction(f'Reaction could not solve for coeffs')

        if np.any(np.abs(coeffs) > 100):
            raise self.SkipReaction(f'Reaction has a coeff over 100')

        if np.any(coeffs < 0.0):
            if not self.allow_gas_release:
                raise self.SkipReaction(f'Reaction has a gas release')
            else:
                if not set(np.array(self.reduced_formulas)[coeffs < 0.0]).issubset(GAS_RELEASE):
                    raise self.SkipReaction(f'Reaction gas releases are not expected gases')

        removed_coeff_indexes = []
        for i in reversed(range(len(coeffs))):
            if np.abs(coeffs[i]) < 0.00001:
                c.pop(i)
                coeffs = np.delete(coeffs, i)
                removed_coeff_indexes.append(i)

        effective_rank = scipy.linalg.lstsq(np.vstack(c).T, target_c)[2]
        if effective_rank < len(coeffs):
            # Removes under-determined reactions.
            # print(effective_rank, precursor_formulas, \
            # [prec_.composition.reduced_formula for prec_ in precursors],coeffs)
            raise self.SkipReaction(f'Reaction is under-determined')

        main_formulas = np.array([
            p for i, p in enumerate(self.reduced_formulas) if i not in removed_coeff_indexes
        ])
        return coeffs, removed_coeff_indexes, main_formulas


class Reactions:

    def __init__(
            self,
            target_entry: ComputedStructureEntry,
            elements: List[str],
            precursor_library: List[ComputedStructureEntry],
            allow_gas_release: bool = False
    ):
        self.target_entry = target_entry
        self.elements = elements
        self.precursor_library = precursor_library
        self.allow_gas_release = allow_gas_release

    def get_reactions(self) -> Dict:
        reactions_dict = {}

        results_by_reduced_formulas = dict()

        for precursors in tqdm(
                itertools.combinations(self.precursor_library, len(self.elements)),
                total=comb(len(self.precursor_library), len(self.elements)),
        ):
            try:
                sorted_precursors = sorted(precursors, key=get_reduced_formula)
                reaction = Reaction(sorted_precursors, self.target_entry, self.elements, self.allow_gas_release)

                if reaction.reduced_formulas not in results_by_reduced_formulas:
                    results_by_reduced_formulas[reaction.reduced_formulas] = reaction.get_balanced_reaction()

                coeffs, removed_coeff_indexes, main_formulas = results_by_reduced_formulas[reaction.reduced_formulas]

                main_precursors = [p for i, p in enumerate(sorted_precursors) if i not in removed_coeff_indexes]
                entry_ids = [str(e.entry_id) for e in main_precursors]
                label = "_".join(sorted(entry_ids))
                if label in reactions_dict:
                    continue
                else:
                    reactions_dict[label] = {
                        "precursors": deepcopy(main_precursors),
                        "coeffs": coeffs,
                        "precursor_formulas": main_formulas,
                        "precursor_ids": entry_ids,
                    }

            except Reaction.SkipReaction as e:
                logger.debug("Skipping precursors %s: %s", precursors, e)
                continue

        logger.info(f"Total # of balanced reactions obtained: {len(reactions_dict)}")
        return reactions_dict
