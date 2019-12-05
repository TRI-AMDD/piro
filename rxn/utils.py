import pandas as pd
import os
import pickle
import numpy as np
from copy import deepcopy

from pymatgen.analysis.substrate_analyzer import SubstrateAnalyzer
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty, Stoichiometry, ValenceOrbital, IonProperty
from matminer.featurizers.structure import (SiteStatsFingerprint, StructuralHeterogeneity,
                                            ChemicalOrdering, StructureComposition, MaximumPackingEfficiency)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances

from joblib import Parallel, delayed

from rxn.data import ST, H
from rxn import RXN_FILES


def get_v(c, elts):
    return np.array([c.as_dict()[el] for el in elts])


def epitaxy(_parents, target):
    def _func(s, target):
        sa = SubstrateAnalyzer(film_max_miller=2, substrate_max_miller=2)
        min_areas = []
        gen = list(sa.calculate(s, target))
        if gen:
            return min([e['match_area'] for e in gen])
        else:
            return 1000000.0

    return Parallel(n_jobs=-1, verbose=1)(delayed(_func)(s, target) for s in _parents)


def similarity(_parents, target):
    featurizer = MultipleFeaturizer([
        SiteStatsFingerprint.from_preset("CoordinationNumber_ward-prb-2017"),
        StructuralHeterogeneity(),
        ChemicalOrdering(),
        MaximumPackingEfficiency(),
        SiteStatsFingerprint.from_preset("LocalPropertyDifference_ward-prb-2017"),
        StructureComposition(Stoichiometry()),
        StructureComposition(ElementProperty.from_preset("magpie")),
        StructureComposition(ValenceOrbital(props=['frac'])),
        StructureComposition(IonProperty(fast=True))
    ])

    x_target = pd.DataFrame.from_records([featurizer.featurize(target)], columns=featurizer.feature_labels())
    x_parent = pd.DataFrame.from_records(featurizer.featurize_many(_parents, ignore_errors=True, pbar=False),
                                         columns=featurizer.feature_labels())
    nulls = x_parent[x_parent.isnull().any(axis=1)].index.values
    x_parent.fillna(100000, inplace=True)

    x_target = x_target.reindex(sorted(x_target.columns), axis=1)
    x_parent = x_parent.reindex(sorted(x_parent.columns), axis=1)

    with open(os.path.join(RXN_FILES, 'scaler.pickle'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(RXN_FILES, 'quantiles.pickle'), 'rb') as f:
        quantiles = pickle.load(f)

    X = scaler.transform(x_parent.append(x_target))

    D = [pairwise_distances(np.array([row, X[-1]]))[0, 1] for row in X[:-1]]

    _res = []
    for d in D:
        _res.append(np.linspace(0, 1, 101)[np.abs(quantiles - d).argmin()])
    _res = np.array(_res)
    _res[nulls] = -1
    return _res


def update_gases(entries, T, P=1, copy=False):
    if copy:
        _entries = deepcopy(entries)
    else:
        _entries = entries
    for e in _entries:
        if e.composition.reduced_formula in ST:
            if isinstance(P, dict):
                P = P.get(e.composition.reduced_formula, 1.0)
            e.data['formation_energy_per_atom'] = H.get(e.composition.reduced_formula,0.0)\
                                                  -ST[e.composition.reduced_formula][T]\
                                                  +8.6173324e-5*T*np.log(P)
    return _entries


def recompute_flatd(source='camd/shared-data/oqmd1.2_icsd_featurized_clean_v2.pickle'):
    from camd import S3_CACHE
    x_all = pd.read_pickle(os.path.join(S3_CACHE, source))
    x_all = x_all.drop(['Composition', 'N_species', 'delta_e',
                        'pred_delta_e', 'pred_stability'], axis=1, errors='ignore')
    sample_X = x_all.sample(15000)
    scaler = StandardScaler()
    sample_X = scaler.fit_transform(sample_X)
    flatD = pairwise_distances(sample_X).flatten()
    quantiles = np.quantile(flatD, np.linspace(0, 1, 101))
    with open('./files/scaler.pickle', 'wb') as f:
        pickle.dump(scaler, f)
    with open('./files/quantiles.pickle', 'wb') as f:
        pickle.dump(quantiles, f)

if __name__ == "__main__":
    recompute_flatd()