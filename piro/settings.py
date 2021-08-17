import os.path
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    use_cache_db: bool = False
    use_mapi_db: bool = False

    mongodb_uri: Optional[str] = None
    mapi_key: Optional[str] = None

    rxn_files: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'files'
    )


settings = Settings()
