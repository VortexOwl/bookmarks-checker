# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from sqlite3 import connect as sqlite3_connect, Cursor, Connection
from pathlib import Path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import Config
from src.logs import get_smart_logger


class BookmarksDatabase:
    _cfg = Config()
    _db_path = Path("data") / "places.sqlite"
    _log = get_smart_logger()


    @classmethod
    def _connect_database(cls) -> tuple[Connection, Cursor]:
        bookmarks_folder = cls._cfg.bookmarks_folder

        connection = sqlite3_connect(cls._db_path)
        cls._log.debug(msg="Подключение к БД прошло успешно.")
        cls._log.info(msg=f'Начата проверка закладок папки "{bookmarks_folder}"')
        cursor = connection.cursor()
        return connection, cursor


    @classmethod
    def bookmarks_check(cls, cursor: Cursor, id_initial_folder: int) -> str:
        bookmarks_folder = cls._cfg.bookmarks_folder
        
        category_reports: list[str] = []
        separator: str = f"\n{'-' * 93}\n"
        
        bookmarks = cursor.execute(
            "SELECT id FROM moz_bookmarks WHERE parent = ? AND type = 1", 
            (id_initial_folder,),
        ).fetchall()
        categories = cursor.execute(
            "SELECT id, title FROM moz_bookmarks WHERE parent = ? AND type = 2", 
            (id_initial_folder,),
        ).fetchall()
        if categories:
            category_reports.append(
                "\n".join(
                    [
                        f"Initial catalog: {bookmarks_folder}",
                        f"bookmarks: {len(bookmarks)}",
                        f"catalogs: {len(categories)}",
                    ]
                )
            )
        else:
            category_reports.append(
                "\n".join(
                    [
                        f"Initial catalog: {bookmarks_folder}",
                        f"bookmarks: {len(bookmarks)}",
                    ]
                )
            )
        for id_category, title_category in categories:
            bookmarks_in_category = cursor.execute(
                "SELECT guid, title FROM moz_bookmarks WHERE parent = ? AND type = 1", 
                (id_category,),
            ).fetchall()
            catalogs_in_category = cursor.execute(
                "SELECT guid, title FROM moz_bookmarks WHERE parent = ? AND type = 2", 
                (id_category,),
            ).fetchall()
            
            if not bookmarks_in_category:
                continue

            if catalogs_in_category:
                category_reports.append(
                    "\n".join(
                        [
                            title_category,
                            f"bookmarks: {len(bookmarks_in_category)}",
                            f"catalogs: {len(catalogs_in_category)}", 
                        ]
                    )
                )
            else:
                category_reports.append(
                    "\n".join(
                        [
                            title_category,
                            f"bookmarks: {len(bookmarks_in_category)}",
                        ]
                    )
                )
        return separator.join(category_reports)


    @classmethod
    def create_bookmarks_report(cls) -> str:
        bookmarks_folder = cls._cfg.bookmarks_folder

        result_check: str = ""
        conn, cursor = cls._connect_database()
        try:
            if initial_folder := cursor.execute(
                "SELECT id FROM moz_bookmarks WHERE title = ?",
                (bookmarks_folder,),
            ).fetchone():
                result_check = cls.bookmarks_check(cursor=cursor, id_initial_folder=initial_folder[0])
            else:
                cls._log.warning(msg=f'Папка "{bookmarks_folder}" не найдена')
        finally:
            conn.close()
        return result_check