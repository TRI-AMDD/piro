import os
import pytest
from piro.settings import Settings, CacheType


@pytest.fixture
def no_env_variables_for_settings(monkeypatch):
    """ensure that the following are removed for the unit tests"""
    monkeypatch.delenv("CACHE_TYPE", raising=False)
    monkeypatch.delenv("MAPI_KEY", raising=False)
    monkeypatch.delenv("MONGODB_URI", raising=False)
    monkeypatch.delenv("USE_MAPI_DB", raising=False)

    # hard to mock/test the default because windows/unix have different case sensitivity
    monkeypatch.setenv("RXN_FILES", 'rxn_files_path')


def test_defaults(no_env_variables_for_settings):
    s = Settings()

    assert s.dict() == {
        'cache_type': CacheType.FILE_CACHE,
        'mapi_key': '',
        'mongodb_uri': None,
        'rxn_files': 'rxn_files_path',
        'use_mapi_db': False
    }


def test_missing_mongo_uri(no_env_variables_for_settings):
    with pytest.raises(ValueError):
        Settings(cache_type=CacheType.MONGO_CACHE)

    with pytest.raises(ValueError):
        Settings(use_mapi_db=True)
