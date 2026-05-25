from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    __path_user: str = Path.home()
    __browser: str = 'Floorp'
    __profile: str = '92bs352o.default-release'
    path_bookmarks: Path = __path_user / 'AppData' / 'Roaming' / __browser / 'Profiles' / __profile
    bookmarks_folder: str = 'Игры'
    result_file: str = 'Result'