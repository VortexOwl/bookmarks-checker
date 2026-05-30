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
from src.logs import get_smart_logger, SmartLogger
from src.basic_utilities.utilities import creating_necessary_folders


bd: BookmarksDatabase = BookmarksDatabase()
cfg: Config = Config()
log: SmartLogger = get_smart_logger()


async def save_bookmarks_report() -> None:
    """
    Копирует файл базы данных закладок Firefox, формирует отчёт и сохраняет его в файл.

    Логика:
    1. Проверяет и/или копирует файл `places.sqlite` в папку `data` в текущем каталоге.
    2. Вызывает метод `BookmarksDatabase.create_bookmarks_report` для формирования отчёта.
    3. Создаёт папку `docs` (если её нет) и записывает отчёт в файл `<report_file>.txt`.
    """

    database_file: str = cfg.database_file
    report_file: str = cfg.report_file
    report_folder: str = cfg.report_folder
    
    path_bookmarks: Path | None = cfg.path_bookmarks
    path_data_folder: Path = Path.cwd() / "data"
    path_report_folder: Path = Path.cwd() / report_folder
    report_path: Path = Path(report_folder) / f"{report_file}.txt"

    Path.mkdir(path_data_folder, exist_ok=True)
    Path.mkdir(path_report_folder, exist_ok=True)
    
    if path_bookmarks is None:
        log.warning(msg="Указан пустой путь для базы данных закладок.")
        if not isfile(path_data_folder / database_file):
            log.fatal(msg="Отсутствует файл базы данных закладок.")
            return
    else:
        try:
            shutil_copy2(path_bookmarks, path_data_folder / database_file)
        except Exception as err:
            log.fatal(
                msg=(
                    f"Произошла ошибка при копировании: {path_bookmarks}. "
                    f"Ошибка: {err}"
                )
            )
            return

    if not (bookmarks_report := await bd.create_bookmarks_report()):
        log.warning("Отчёт по закладкам пуст, файл не будет создан.")
        return
    
    with report_path.open("w", encoding="utf-8") as file_result:
        file_result.write(bookmarks_report)
    
    log.info(
        msg=(
            "Информация о количестве закладок в категориях "
            f"сохранена в файл: {report_path.name}"
        )
    )
        