from typing import Tuple, List

import pandas as pd
import os
import pickle
import numpy as np
import json
from functools import lru_cache

from pymatgen.core import Structure
from pymatgen.entries.computed_entries import ComputedStructureEntry
from pymongo import MongoClient
from scipy.interpolate import interp1d
from pymatgen.core.composition import Composition
from pymatgen.analysis.substrate_analyzer import SubstrateAnalyzer
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import (
    ElementProperty,
    Stoichiometry,
    ValenceOrbital,
    IonProperty,
)
from matminer.featurizers.structure import (
    SiteStatsFingerprint,
    StructuralHeterogeneity,
    ChemicalOrdering,
    StructureComposition,
    MaximumPackingEfficiency,
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from sklearn.linear_model import LinearRegression

from joblib import Parallel, delayed

from piro.data import ST
from piro.settings import settings, CacheType


def get_v(composition_as_dict: dict, elts: Tuple[str]) -> np.array:
    return np.array([composition_as_dict[el] for el in elts])


def get_epitaxies(
    precursor_library: List[ComputedStructureEntry],
    target: ComputedStructureEntry,
    cache_type: CacheType
):
    if cache_type == CacheType.MONGO_CACHE:
        precursor_set = set([s.entry_id for s in precursor_library])
        epitaxies = {}
        for e in mongo_results_generator(target, 'epitaxies'):
            for material_id in e["material_ids"]:
                if material_id in precursor_set:
                    # If "min_epitaxy" is not in the cached entry, most likely the epitaxy calculation failed.
                    # Assign the high value so they will get discounted.
                    epitaxies[material_id] = float(e.get("min_epitaxy", 1000000.0))

    else:
        precursor_structures = [s.structure for s in precursor_library]
        target_structure = target.structure
        if cache_type == CacheType.FILE_CACHE:
            results = through_cache(precursor_structures, target_structure, epitaxy)
        else:
            results = epitaxy(precursor_structures, target_structure)
        epitaxies = dict(
            zip([i.entry_id for i in precursor_library], results)
        )
        print("Epitaxies ready")

    return epitaxies


def get_similarities(
    precursor_library: List[ComputedStructureEntry],
    target: ComputedStructureEntry,
    cache_type: CacheType
 ):
    if settings.cache_type == CacheType.MONGO_CACHE:
        precursor_set = set([s.entry_id for s in precursor_library])
        similarities = {}
        for s in mongo_results_generator(target, 'similarity'):
            if "similarity" not in s.keys():
                print(f"Missing 'similarity' at:\n {s}")
                continue
            for material_id in s["material_ids"]:
                if material_id in precursor_set:
                    similarities[material_id] = s["similarity"]

    else:
        precursor_structures = [s.structure for s in precursor_library]
        target_structure = target.structure
        if cache_type == CacheType.FILE_CACHE:
            results = through_cache(precursor_structures, target_structure, similarity)
        else:
            results = similarity(precursor_structures, target_structure)

        similarities = dict(zip([i.entry_id for i in precursor_library], results))
        print("similarity matrix ready")

    return similarities


def mongo_results_generator(target: ComputedStructureEntry, collection_name: str):
    with MongoClient(settings.mongodb_uri) as mongo_client:
        for result in mongo_client.piro[collection_name].find({"material_ids": target.entry_id}):
            yield result


def through_cache(_parents: List[Structure], target: Structure, func):

    if not os.path.exists(settings.rxn_files):
        os.mkdir(settings.rxn_files)

    cache_path = os.path.join(settings.rxn_files, "_" + func.__name__ + "_cache.json")
    if os.path.isfile(cache_path):
        with open(cache_path, "r") as f:
            db = json.load(f)
    else:
        db = {}
    ordered_pairs = ["_".join(sorted([target.entry_id, i.entry_id])) for i in _parents]
    indices_compt = [i for i in range(len(ordered_pairs)) if ordered_pairs[i] not in db]

    if indices_compt:
        # Don't use numpy here because structures is iterable
        _res = func([_parents[i] for i in indices_compt], target)
    else:
        _res = []
    results = []
    for i in ordered_pairs:
        if i in db:
            results.append(db[i])
        else:
            results.append(_res[indices_compt.index(ordered_pairs.index(i))])
            db[i] = _res[indices_compt.index(ordered_pairs.index(i))]

    with open(cache_path, "w") as f:
        json.dump(db, f)
    return results


def epitaxy(_parents: List[Structure], target: Structure):
    def _func(s, target):
        sa = SubstrateAnalyzer(film_max_miller=2, substrate_max_miller=2)
        gen = [g for g in sa.calculate(s, target) if g]
        if gen:
            return min([e.match_area for e in gen])
        else:
            return 1000000.0

    # Uncomment to debug SA issues
    # return [_func(s, target) for s in _parents]
    return Parallel(n_jobs=-1, verbose=1)(delayed(_func)(s, target) for s in _parents)


def similarity(_parents: List[Structure], target: Structure):
    featurizer = MultipleFeaturizer(
        [
            SiteStatsFingerprint.from_preset("CoordinationNumber_ward-prb-2017"),
            StructuralHeterogeneity(),
            ChemicalOrdering(),
            MaximumPackingEfficiency(),
            SiteStatsFingerprint.from_preset("LocalPropertyDifference_ward-prb-2017"),
            StructureComposition(Stoichiometry()),
            StructureComposition(ElementProperty.from_preset("magpie")),
            StructureComposition(ValenceOrbital(props=["frac"])),
            StructureComposition(IonProperty(fast=True)),
        ]
    )

    # HACK celery doesn't work with multiprocessing (used by matminer)
    try:
        from celery import current_task
        if current_task:
            featurizer.set_n_jobs(1)
    except ImportError:
        pass

    x_target = pd.DataFrame.from_records(
        [featurizer.featurize(target)], columns=featurizer.feature_labels()
    )
    x_parent = pd.DataFrame.from_records(
        featurizer.featurize_many(_parents, ignore_errors=True, pbar=False),
        columns=featurizer.feature_labels(),
    )
    nulls = x_parent[x_parent.isnull().any(axis=1)].index.values
    x_parent.fillna(100000, inplace=True)

    x_target = x_target.reindex(sorted(x_target.columns), axis=1)
    x_parent = x_parent.reindex(sorted(x_parent.columns), axis=1)

    with open(os.path.join(settings.rxn_files, "scaler2.pickle"), "rb") as f:
        scaler = pickle.load(f)
    with open(os.path.join(settings.rxn_files, "quantiles.pickle"), "rb") as f:
        quantiles = pickle.load(f)

    X = scaler.transform(pd.concat([x_parent, x_target], axis=0))

    D = [pairwise_distances(np.array([row, X[-1]]))[0, 1] for row in X[:-1]]

    _res = []
    for d in D:
        _res.append(np.linspace(0, 1, 101)[np.abs(quantiles - d).argmin()])
    _res = np.array(_res)
    _res[nulls] = -1
    return _res


@lru_cache()
def get_ST(c, T):
    f = interp1d(np.fromiter(ST[c].keys(), dtype=float),
                 np.fromiter(ST[c].values(), dtype=float),
                 bounds_error=True)
    return f(T)


def recompute_flatd(source="camd/shared-data/oqmd1.2_icsd_featurized_clean_v2.pickle"):
    from camd import S3_CACHE

    x_all = pd.read_pickle(os.path.join(S3_CACHE, source))
    x_all = x_all.drop(
        ["Composition", "N_species", "delta_e", "pred_delta_e", "pred_stability"],
        axis=1,
        errors="ignore",
    )
    sample_X = x_all.sample(15000)
    scaler = StandardScaler()
    sample_X = scaler.fit_transform(sample_X)
    flatD = pairwise_distances(sample_X).flatten()
    quantiles = np.quantile(flatD, np.linspace(0, 1, 101))
    with open("./files/scaler2.pickle", "wb") as f:
        pickle.dump(scaler, f)
    with open("./files/quantiles2.pickle", "wb") as f:
        pickle.dump(quantiles, f)


def oqmd_to_mp_compatible_energy(composition, energy, mp=None, oqmd=None):
    """
    Helper method to get an ad hoc adjustment to an OQMD formation energy (eV/atom)
    given two dictionaries with compositions as keys and formation energies as
    values for a set of matching structures across both databases.
    A linear (per-atom) adjustment is found.
    """
    c = Composition(composition).fractional_composition.as_dict()
    elems = sorted(c.keys())
    x, y = [], []
    for i in mp:
        c1 = Composition(i).fractional_composition.as_dict()
        x.append([c1[el] for el in elems])
        y.append(mp[i] - oqmd[i])
    reg = LinearRegression()
    reg.fit(x, y)
    return energy + reg.predict([[c[el] for el in elems]])[0]


if __name__ == "__main__":
    recompute_flatd()
