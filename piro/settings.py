import os
from enum import Enum
from typing import Optional
from pydantic import BaseSettings, validator


class CacheType(str, Enum):
    NO_CACHE = 'no_cache'
    FILE_CACHE = 'file_cache'
    MONGO_CACHE = 'mongo_cache'


class Settings(BaseSettings):
    mongodb_uri: Optional[str] = None
    mapi_key: str = ''
    rxn_files: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'files'
    )

    cache_type: CacheType = CacheType.FILE_CACHE
    use_mapi_db: bool = False

    @validator('mapi_key')
    def update_env_with_mapi_key(cls, v):
        if v and not os.environ.get('MAPI_KEY'):
            os.environ['MAPI_KEY'] = v
        return v

    @validator('cache_type')
    def check_cache_type(cls, v, values):
        if v == CacheType.MONGO_CACHE:
            if not values.get('mongodb_uri'):
                raise ValueError('MONGODB_URI must be provided when using mongo cache.')
        return v

    @validator('use_mapi_db')
    def check_mongo_uri_exists_for_mapi_db(cls, v, values):
        if v:
            if not values.get('mongodb_uri'):
                raise ValueError('MONGODB_URI must be provided when using mapi DB.')
        return v

    class Config:
        allow_mutation = False


settings = Settings()
