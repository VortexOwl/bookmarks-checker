# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import run as async_run

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from basic_utilities.base_config_project import add_workdir_in_PATH
add_workdir_in_PATH()
from src.bookmarks.report import save_bookmarks_report


def start() -> None:
    """Точка входа: запускает асинхронное сохранение отчёта по закладкам."""
    async_run(save_bookmarks_report())
    

if __name__ == "__main__":
    start()
