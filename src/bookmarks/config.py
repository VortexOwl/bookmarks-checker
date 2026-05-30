# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from dataclasses import dataclass
from pathlib import Path
from platform import system


@dataclass
class Config:
    __sys = system()
    __path_user: Path = Path.home()
    __browser: str = 'Floorp'
    if __sys == "Windows":
        __browser = 'AppData' / 'Roaming' / __browser / 'Profiles'
    elif __sys == "Linux":
        __browser = '.floorp'
    __profile: str = 'kcs8yk9h.default-default'
    
    path_bookmarks: Path = __path_user / __browser / __profile
    bookmarks_folder: str = 'KDE Store'
    result_file: str = 'Result'
