# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import isfile
from shutil import copy2 as shutil_copy2
from pathlib import Path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import Config
from src.bookmarks.database import BookmarksDatabase
from src.logs import get_smart_logger
from src.basic_utilities.utilities import creating_necessary_folders


log = get_smart_logger()
cfg = Config()
bd = BookmarksDatabase()


def save_files() -> None:
    path: Path = cfg.path_bookmarks
    result_file: str = cfg.result_file
    path_data_folder: str = Path.cwd() / "data"
    database_file: str = "places.sqlite"
    Path.mkdir(path_data_folder, exist_ok=True)
    
    if path == "":
        log.warning(msg="Указан пустой путь для базы данных закладок.")
        if not isfile(path_data_folder / database_file):
            log.fatal(msg="Отсутствует файл базы данных закладок.")
            return
    else:
        try:
            shutil_copy2(path / database_file, path_data_folder / database_file)
        except Exception:
            log.fatal(
                msg=(
                    "Указан неверный путь к файлу базы данных закладок: "
                    f"{path / database_file}"
                )
            )
            return

    if not (bookmarks_report := bd.create_bookmarks_report()):
        return
    
    creating_necessary_folders("docs")
    with open(Path("docs") / f"{result_file}.txt", "w", encoding="utf-8") as file_result:
        file_result.write(bookmarks_report)
    log.info(
        msg=(
            "Информация о количестве закладок в категориях "
            f"сохранена в файл: {result_file}.txt"
        )
    )
        