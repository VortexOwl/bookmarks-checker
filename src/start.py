# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from basic_utilities.base_config_project import add_workdir_in_PATH
add_workdir_in_PATH()
from src.bookmarks.report import save_files


def start() -> None:
    save_files()
    

if __name__ == "__main__":
    start()
