# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import isfile
from shutil import copy2 as shutil_copy2

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import path_bookmarks, name_text_file
from src.bookmarks.database import create_bookmarks_report
from src.logs import get_smart_logger
from src.basic_utilities.utilities import creating_necessary_folders


log = get_smart_logger()



def save_files() -> None:
    if path_bookmarks == "":
        log.warning(msg="Указан пустой путь для файла закладок.")
        if not isfile("data/places.sqlite"):
            log.fatal(msg="Отсутствует файл базы данных закладок.")
            return
    else:
        try:
            shutil_copy2(f"{path_bookmarks}/places.sqlite", "data/places.sqlite")
        except Exception:
            log.fatal(
                msg=(
                    "Указан неверный путь к файлу базы данных закладок. "
                    f"{path_bookmarks}/places.sqlite"
                )
            )
            return

    if not (bookmarks_report := create_bookmarks_report()):
        return
    creating_necessary_folders("docs")
    with open(f"docs/{name_text_file}.txt", "w", encoding="utf-8") as file_result:
        file_result.write(bookmarks_report)
    log.info(
        msg=(
            "Информация о количестве закладок в категориях "
            f"сохранена в файл: {name_text_file}.txt"
        )
    )
        