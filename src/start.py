# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from asyncio import run as async_run

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities.basic_utilities_project import add_workdir_in_PATH
add_workdir_in_PATH()
from src.app import ApplicationService


def start() -> None:
    """Точка входа: запускает асинхронное сохранение отчёта по закладкам."""
    
    async_run(ApplicationService.save_bookmarks_report(is_save_file=True))


def start_clear() -> None:
    """Точка входа: запускает асинхронное очищение от файлов директории для формирования отчётов."""
    
    async_run(ApplicationService.clear_report_files())


if __name__ == "__main__":
    start()
