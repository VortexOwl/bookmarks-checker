# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from sqlite3 import connect as sqlite3_connect, Cursor, Connection

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import name_bookmarks_folder
from src.logs import get_smart_logger

log = get_smart_logger()


def connect_database() -> tuple[Connection, Cursor]:
    connection = sqlite3_connect("data/places.sqlite")
    log.debug(message="Подключение к БД прошло успешно.")
    log.info(message=f'Начата проверка закладок папки "{name_bookmarks_folder}"')
    cursor = connection.cursor()
    return connection, cursor


def bookmarks_check(cursor: Cursor, id_initial_folder: int) -> str:
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
                    f"Initial catalog: {name_bookmarks_folder}",
                    f"bookmarks: {len(bookmarks)}",
                    f"catalogs: {len(categories)}",
                ]
            )
        )
    else:
        category_reports.append(
            "\n".join(
                [
                    f"Initial catalog: {name_bookmarks_folder}",
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


def create_bookmarks_report() -> str:
    result_check: str = ""
    conn, cursor = connect_database()
    try:
        if initial_folder := cursor.execute(
            "SELECT id FROM moz_bookmarks WHERE title = ?",
            (name_bookmarks_folder,),
        ).fetchone():
            result_check = bookmarks_check(cursor=cursor, id_initial_folder=initial_folder[0])
        else:
            log.warning(message=f'Папка "{name_bookmarks_folder}" не найдена')
    finally:
        conn.close()
    return result_check