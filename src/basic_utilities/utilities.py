# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os import mkdir
from os.path import isdir


def creating_necessary_folders(path:str) -> None:
    if not isdir(s=path):
        mkdir(path=path)


def read_file_line_by_line(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

