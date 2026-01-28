# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from sqlite3 import connect as sqlite3_connect, Cursor

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import name_bookmarks_folder
from src.logs import log_debug, log_info, log_warning


def connection_database() -> Cursor | None:
    with sqlite3_connect('data/places.sqlite') as connection:
        log_debug(message='Подключение к БД прошло успешно.')
        log_info(
            message=f'Начата проверка закладок папки "{name_bookmarks_folder}"'
            )
        cursor = connection.cursor()
        return cursor
    return None


def bookmarks_check(cursor:Cursor) -> str:
    bookmarks_in_category_count = list()
    initial_folder = cursor.execute(
        f"select id from moz_bookmarks where title='{name_bookmarks_folder}'"
        ).fetchone()
    if initial_folder:
        id_initial_folder = initial_folder[0]
        bookmarks = cursor.execute(
            f"select id from moz_bookmarks "\
            f"where parent={id_initial_folder} and type=1").fetchall()
        categories = cursor.execute(
            f"select id, title from moz_bookmarks "\
            f"where parent={id_initial_folder} and type=2").fetchall()
        if categories:
            bookmarks_in_category_count.append(
                '\n'.join([
                    f'Initial catalog: {name_bookmarks_folder}',
                    f'bookmarks: {len(bookmarks)}',
                    f'catalogs: {len(categories)}']))
        else:
            bookmarks_in_category_count.append(
                '\n'.join([
                    f'Initial catalog: {name_bookmarks_folder}',
                    f'bookmarks: {len(bookmarks)}']))
        for category in categories:
            id_category, title_category = category
            bookmarks_in_category = cursor.execute(
                f"select guid, title from moz_bookmarks "\
                f"where parent={id_category} and type=1").fetchall()
            catalogs_in_category = cursor.execute(
                f"select guid, title from moz_bookmarks "\
                f"where parent={id_category} and type=2").fetchall()
            if bookmarks_in_category:
                if catalogs_in_category:
                    bookmarks_in_category_count.append(
                        '\n'.join([
                            title_category,
                            f'bookmarks: {len(bookmarks_in_category)}',
                            f'catalogs: {len(catalogs_in_category)}']))
                else:
                    bookmarks_in_category_count.append(
                        '\n'.join([
                            title_category,
                            f'bookmarks: {len(bookmarks_in_category)}']))
    else:
        log_warning(message=f'Папка "{name_bookmarks_folder}" не найдена')
    return f'\n{93*'-'}\n'.join(bookmarks_in_category_count)