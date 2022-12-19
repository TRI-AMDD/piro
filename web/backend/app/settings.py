import pathlib
import piro.settings


class Settings(piro.settings.Settings):
    host: str = '0.0.0.0'
    port: int = 8080

    enable_react: bool = False
    react_build_dir: str = str((pathlib.Path(__file__).parent.parent.parent / 'frontend' / 'build').resolve())

    class Config:
        env_file = str((pathlib.Path(__file__).parent.parent / '.env').resolve())
