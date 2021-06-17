from piro import MONGODB_URI
from pymongo import MongoClient


_client = None


def _init_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client


def query_epitaxies(precursor_set, target_id):
    """
    Query the cached epitaxies from the database.

    Args:
        precursor_set (set[str]): the set of precursor library id
        target_id (str): the target material id

    Return:
        The epitaxies dictionary with the key is material id and the value is min epitaxy.
    """
    _init_mongo_client()
    epitaxies = dict()
    for e in _client.piro.epitaxies.find({"material_ids": target_id}):
        for material_id in e["material_ids"]:
            if material_id in precursor_set:
                # If "min_epitaxy" is not in the cached entry, most likely the epitaxy calculation failed.
                # Assign the high value so they will get discounted.
                epitaxies[material_id] = float(e.get("min_epitaxy", 1000000.0))
    return epitaxies


def query_similarities(precursor_set, target_id):
    """
    Query the cached similarities from the database.

    Args:
        precursor_set (set[str]): the set of precursor library id
        target_id (str): the target material id

    Return:
        The similarities dictionary with the key is material id and the value is similarity.
    """
    _init_mongo_client()
    similarities = dict()
    for s in _client.piro.similarity.find({"material_ids": target_id}):
        if "similarity" not in s.keys():
            print(f"Missing 'similarity' at:\n {s}")
            continue
        for material_id in s["material_ids"]:
            if material_id in precursor_set:
                similarities[material_id] = s["similarity"]
    return similarities
