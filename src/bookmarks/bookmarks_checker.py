# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import isfile
from shutil import copy2 as shutil_copy2

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import path_bookmarks, name_text_file
from src.bookmarks.database import connection_database, bookmarks_check
from src.logs import log_info, log_warning, log_fatal
from utilities.utilities import creating_necessary_folders


def start_bookmarks_checker() -> None:
    if path_bookmarks == '':
        log_warning(message='Указан пустой путь для файла закладок.')
        if not isfile('data/places.sqlite'):
            log_fatal(message='Отсутствует файл базы данных закладок.')
    else:
        shutil_copy2(f'{path_bookmarks}/places.sqlite', 'data/places.sqlite')
        
    cursor = connection_database()
    if cursor:
        folder_bookmark_count = bookmarks_check(cursor=cursor)
        creating_necessary_folders('docs')
        file_result = open(f'docs/{name_text_file}.txt', 'w', encoding='utf-8')
        file_result.write(folder_bookmark_count)
        log_info(
            message=f'Информация о количестве закладок в категориях '\
            'сохранена в файл: {name_text_file} .txt')
    else:
        log_fatal('Возникла ошибка подключения к базе данных закладок.')