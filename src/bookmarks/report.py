# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import to_thread as asyncio_to_thread
from os.path import isfile
from pathlib import Path
from shutil import copy2 as shutil_copy2

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.basic_utilities.utilities import creating_necessary_folders
from src.bookmarks.config import Config
from src.bookmarks.database import BookmarksDatabase
from src.logs import get_smart_logger, SmartLogger


bd: BookmarksDatabase = BookmarksDatabase()
log: SmartLogger = get_smart_logger()


async def _save_db_in_data(cfg: Config) -> str | None:
    """
    Проверяет и/или копирует файл `places.sqlite` в папку `data` в текущем каталоге.
    """
    database_file: str = cfg.database_file

    path_bookmarks: Path | None = cfg.path_bookmarks
    path_data_folder: Path = Path.cwd() / "data"

    Path.mkdir(path_data_folder, exist_ok=True)


    if path_bookmarks is None:
        log.warning(msg="Указан пустой путь для базы данных закладок.")
        if not isfile(path_data_folder / database_file):
            err = "По указанному пути отсутствует файл базы данных закладок."
            log.fatal(msg=err)
            return err
        log.info(msg="Проверяется старый файл базы данных закладок.")
    else:
        try:
            shutil_copy2(path_bookmarks, path_data_folder / database_file)
        except FileNotFoundError:
            err = "По указанному пути отсутствует файл базы данных закладок."
            log.fatal(msg=err)
            return err
        except Exception as err:
            log.fatal(
                msg=(
                    f"Произошла ошибка при копировании: {path_bookmarks}. "
                    f"Ошибка: {type(err)} {err}"
                )
            )
            return err
    return None


async def save_bookmarks_report(
    is_save_file: bool, 
    cfg: Config | None = None
) -> tuple[str | None, Path | None, str | None]:
    """
    Копирует файл базы данных закладок Firefox, формирует отчёт и сохраняет его в файл.

    Логика:
    1. Проверяет и/или копирует файл `places.sqlite` в папку `data` в текущем каталоге.
    2. Вызывает метод `BookmarksDatabase.create_bookmarks_report` для формирования отчёта.
    3. Создаёт папку `docs` (если её нет) и записывает отчёт в файл `<report_file>.txt`.
    """
    if cfg is None:
        cfg = Config()
        cfg.update_config()
    
    report_file: str = cfg.report_file
    report_folder: str = cfg.report_folder
    path_report_folder: Path
    report_path: Path
    
    if err := await _save_db_in_data(cfg=cfg):
        return None, None, err

    if not (bookmarks_report := await bd.create_bookmarks_report(cfg=cfg)):
        err = "Указанная директория отсутствует в базе данных закладок."
        log.warning(msg=err)
        return None, None, err
    
    if is_save_file:
        path_report_folder = Path.cwd() / report_folder
        report_path = Path(report_folder) / f"{report_file}.txt"

        Path.mkdir(path_report_folder, exist_ok=True)

        with report_path.open("w", encoding="utf-8") as file_result:
            file_result.write(bookmarks_report)
        
        log.info(
            msg=(
                "Информация о количестве закладок в категориях "
                f"сохранена в файл: {report_path.name}"
            )
        )
        return bookmarks_report, report_path, None
    
    return bookmarks_report, None, None


async def clear_report_files(cfg : Config = Config()) -> dict[str, int | str, tuple[str]]:
    """
    Асинхронно и безопасно очищает папку от файлов.
    Возвращает статистику по успешным удалениям и ошибкам.
    """
    report_folder: str = cfg.report_folder
    path_report_folder = Path.cwd() / report_folder
    
    if not path_report_folder.exists() or not path_report_folder.is_dir():
        name_err = f"Путь не существует или не является папкой: {path_report_folder}"
        log.warning(msg=name_err)
        return {"success": 0, "errors": 1, "names of errors": (name_err)}

    stats = {"success": 0, "errors": 0}
    names_err = set()

    for file_name in path_report_folder.iterdir():
        try:
            if file_name.is_file():
                await asyncio_to_thread(file_name.unlink, missing_ok=True)
                stats["success"] += 1

        except PermissionError:
            name_err = f"Нет прав на удаление файла: {file_name}"
            log.error(msg=name_err)
            stats["errors"] += 1
            names_err.add(name_err)

        except FileNotFoundError:
            pass
            
        except Exception as err:
            name_err = f"Не удалось удалить {file_name}. Ошибка: {err}"
            log.exception(msg=name_err)
            stats["errors"] += 1
            names_err.add(name_err)
    
    stats["names of errors"] = tuple(names_err)
    log.info(msg="Директория для отчетов была успешно очищена от файлов.")
    log.debug(msg=f"Сводка выполнения очистки:\n{stats}")
    return stats
