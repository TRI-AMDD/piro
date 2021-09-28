import os
import piro.settings


class Settings(piro.settings.Settings):
    host: str = '0.0.0.0'
    port: int = 8080

    enable_react: bool = False
    react_build_dir: str = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        'frontend',
        'build'
    )

    class Config:
        env_file = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            '.env'
        )
