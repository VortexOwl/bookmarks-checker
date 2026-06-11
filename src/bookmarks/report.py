# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import isfile
from pathlib import Path
from shutil import copy2 as shutil_copy2

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import Config
from src.bookmarks.database import BookmarksDatabase
from src.logs import get_smart_logger, SmartLogger
from src.utilities import Utilities as uts


class Report:
    _bd: BookmarksDatabase = BookmarksDatabase()
    _log: SmartLogger = get_smart_logger()

    @classmethod
    def _save_db_in_data(cls, cfg: Config) -> str | None:
        """
        Проверяет и/или копирует файл `places.sqlite` в папку `data` в текущем каталоге.
        """
        database_file: str = cfg.database_file

        path_bookmarks: Path | None = cfg.path_bookmarks
        path_data_folder: Path = Path.cwd() / "data"

        Path.mkdir(path_data_folder, exist_ok=True)

        if path_bookmarks is None:
            cls._log.warning(msg="Указан пустой путь для базы данных закладок.")
            if not isfile(path_data_folder / database_file):
                err = "По указанному пути отсутствует файл базы данных закладок."
                cls._log.fatal(msg=err)
                return err
            cls._log.info(msg="Проверяется старый файл базы данных закладок.")
        else:
            try:
                shutil_copy2(path_bookmarks, path_data_folder / database_file)
            except FileNotFoundError:
                err = "По указанному пути отсутствует файл базы данных закладок."
                cls._log.fatal(msg=err)
                return err
            except Exception as err:
                cls._log.fatal(
                    msg=(
                        f"Произошла ошибка при копировании: {path_bookmarks}. "
                        f"Ошибка: {type(err)} {err}"
                    )
                )
                return err
        return None

    @classmethod
    async def save_bookmarks_report(
        cls,
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
        report_file: str = cfg.report_file
        report_folder: str = cfg.report_folder
        path_report_folder: Path
        report_path: Path
        
        if cfg is None:
            cfg = Config()
            cfg.update_config()
        
        if err := cls._save_db_in_data(cfg=cfg):
            return None, None, err

        if not (bookmarks_report := await cls._bd.create_bookmarks_report(cfg=cfg)):
            err = "Указанная директория отсутствует в базе данных закладок."
            cls._log.warning(msg=err)
            return None, None, err
        
        if is_save_file:
            path_report_folder = Path.cwd() / report_folder
            report_path = path_report_folder / f"{report_file}.txt"

            Path.mkdir(path_report_folder, exist_ok=True)

            with report_path.open("w", encoding="utf-8") as file_result:
                file_result.write(bookmarks_report)
            
            cls._log.info(
                msg=(
                    "Информация о количестве закладок в категориях "
                    f"сохранена в файл: {report_path.name}"
                )
            )
            return bookmarks_report, report_path, None
        
        return bookmarks_report, None, None

    @staticmethod
    async def clear_report_files(cfg : Config = Config()) -> dict[str, int | tuple[str]]:
            """
            Асинхронно и безопасно очищает папку от файлов.
            Возвращает статистику по успешным удалениям и ошибкам.
            """
            return await uts.clearing_folder(clear_folder=cfg.report_folder)
