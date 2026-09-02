# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from dataclasses import dataclass
from os import getenv
from pathlib import Path
from platform import system
from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    host: str = getenv('API_HOST', '0.0.0.0') if Path('/.dockerenv').exists() else getenv('API_HOST', '127.0.0.1')
    port: int = getenv('API_PORT', 8000)
    is_reload: bool = getenv('API_IS_RELOAD', False) if Path('/.dockerenv').exists() else getenv('API_IS_RELOAD', True)


class Config(BaseSettings):
    """
    Конфигурация для проведения анализа директории закладок браузера.
    """
    log_level: int = 10
    is_open_webbrowser: bool = getenv('IS_OPEN_WEBBROWSER', True)
    bookmarks_folder: str = getenv('APP_BOOKMARKS_TAG', 'KDE Store')
    report_folder: str = getenv('APP_REPORT_FOLDER', 'docs')
    data_folder: str = getenv('APP_DATA_FOLDER', 'data')
    database_file: str = 'places.sqlite'
    browser: str = getenv('APP_BROWSER', 'Floorp')
    _default_profile_pattern: str = '*.default-default'
    custom_report_file: str | None = None
    browser_profile: str | None = None

    @property
    def path_data_folder(self) -> Path:
        return Path(self.data_folder) / self.database_file

    @property
    def report_file(self) -> str:
        return (
            f'Bookmarks {self.bookmarks_folder}'
            if self.custom_report_file is None
            else self.custom_report_file
        )
    @property
    def is_docker(self) -> bool:
        return Path('/.dockerenv').exists()

    @property
    def path_source_database(self) -> Path | None:
        sys_name = system()
        path_user: Path = Path.home()
        path_browser: Path = Path(self.browser)
        path_profiles: Path
        path_profile_bookmarks: Path        

        if sys_name == 'Windows':
            path_browser = Path('AppData') / 'Roaming' / path_browser / 'Profiles'
        elif sys_name == 'Linux':
            path_browser = Path(getenv('APP_BROWSER_FOLDER', '.floorp'))
        else:
            return None

        path_profiles = path_user / path_browser

        if self.browser_profile is not None:
            path_profile_bookmarks = path_profiles / self.browser_profile
        else:
            default_profile: Path = next(
                (d for d in path_profiles.glob(self._default_profile_pattern) if d.is_dir()), 
                None,
            )
            if default_profile is None:
                return None
            path_profile_bookmarks = default_profile
    
        return path_profile_bookmarks / self.database_file