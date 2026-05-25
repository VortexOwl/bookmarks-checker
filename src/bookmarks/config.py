from dataclasses import dataclass


@dataclass
class Config:
    path_bookmarks = '/home/dmitry/.mozilla/firefox/ooln9kd9.default-release/'          # Путь к файлу закладок FireFox
    name_bookmarks_folder = 'Фильмы'                                                    # Название папки закладок
    result_file = 'Result'                                                              # Название текстового файла