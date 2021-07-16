import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8080

    mapi_key: str

    enable_react: bool = True
    react_build_dir: str = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        'frontend',
        'build'
    )

    use_cache_db: bool = False
    mongdb_uri: str = ''

    class Config:
        env_file = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            '.env'
        )
