# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from dataclasses import dataclass
from pathlib import Path
from platform import system


@dataclass
class Config:
    """
    Конфигурация для проверки закладок Floorp.
    """

    bookmarks_folder: str = 'KDE Store'
    report_folder: str = 'docs'
    report_file: str = f'Bookmarks {bookmarks_folder}'
    database_file: str = 'places.sqlite'
    browser: Path = Path('Floorp')
    custom_profile: Path | None = None
    path_bookmarks: Path | None = None
    
    
    def __post_init__(self) -> None:  # sourcery skip: move-assign
        sys_name = system()
        path_user: Path = Path.home()
        default_profile_pattern: str = '*.default-default'
        path_browser: Path | None = self.browser
        path_profiles: Path
        path_profile_bookmarks: Path

        if sys_name == 'Windows':
            path_browser = Path('AppData') / 'Roaming' / path_browser / 'Profiles'
        elif sys_name == 'Linux':
            path_browser = Path('.floorp')
        else:
            path_browser = None
            self.path_bookmarks = None
            return

        path_profiles = path_user / path_browser

        if self.custom_profile is not None:
            path_profile_bookmarks = path_profiles / self.custom_profile
        else:
            default_profile: Path = next(
                (d for d in path_profiles.glob(default_profile_pattern) if d.is_dir()), 
                None,
            )
            if default_profile is None:
                self.path_bookmarks = None
                return
            path_profile_bookmarks = default_profile
    
        self.path_bookmarks = path_profile_bookmarks / self.database_file
