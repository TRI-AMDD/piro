import os

import pytest

from piro.settings import Settings, CacheType


def test_defaults():
    s = Settings()

    assert s.dict() == {
        'cache_type': CacheType.FILE_CACHE,
        'mapi_key': None,
        'mongodb_uri': None,
        'rxn_files': s.rxn_files,  # TODO mock this
        'use_mapi_db': False
    }


def test_missing_mongo_uri():
    with pytest.raises(ValueError):
        Settings(cache_type=CacheType.MONGO_CACHE)

    with pytest.raises(ValueError):
        Settings(use_mapi_db=True)
