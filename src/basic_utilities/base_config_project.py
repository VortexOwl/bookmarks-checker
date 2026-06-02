# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import dirname, abspath
from sys import path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from basic_utilities.config import BaseConfig


def add_workdir_in_PATH() -> None:
    if BaseConfig.is_not_active:
        path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
        if BaseConfig.is_console_debug:
            print(f'Working folder: {dirname(dirname(dirname(abspath(__file__))))}')
