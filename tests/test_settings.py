from pathlib import Path

import pytest

from piro.settings import Settings, CacheType


@pytest.fixture
def no_env_variables_for_settings(monkeypatch):
    """ensure that the following are removed for the unit tests"""
    monkeypatch.delenv("CACHE_TYPE", raising=False)
    monkeypatch.delenv("MAPI_KEY", raising=False)
    monkeypatch.delenv("MONGODB_URI", raising=False)
    monkeypatch.delenv("RXN_FILES", raising=False)
    monkeypatch.delenv("USE_MAPI_DB", raising=False)


def test_defaults(no_env_variables_for_settings):
    s = Settings()

    assert s.dict() == {
        'cache_type': CacheType.FILE_CACHE,
        'mapi_key': '',
        'mongodb_uri': None,
        'rxn_files': str(Path(__file__).parent.parent / 'piro' / 'files'),
        'use_mapi_db': False
    }


def test_missing_mongo_uri(no_env_variables_for_settings):
    with pytest.raises(ValueError):
        Settings(cache_type=CacheType.MONGO_CACHE)

    with pytest.raises(ValueError):
        Settings(use_mapi_db=True)
