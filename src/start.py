# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities import base_config_project
from src.bookmarks.bookmarks_checker import start_bookmarks_checker


def start() -> None:
    start_bookmarks_checker()
    

start()
