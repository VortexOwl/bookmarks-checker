# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities import base_config_project
from src.bookmarks_checker import bookmarks_check


def start() -> None:
    bookmarks_check()

start()