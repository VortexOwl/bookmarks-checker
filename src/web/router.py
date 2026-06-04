# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from copy import copy
from enum import Enum
from pydantic import BaseModel
from typing import Annotated, Literal

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import Config
from src.bookmarks.report import save_bookmarks_report, clear_report_files

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, Form, Depends, Query
from fastapi.responses import Response, FileResponse, PlainTextResponse
from uvicorn import run as uvicorn_run


web = FastAPI(
    title="📚 Bookmarks API", 
    swagger_ui_parameters = {
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "filter": True,
        "displayRequestDuration": True
    }
)

cfg = Config()


class Browser(str, Enum):
    FLOORP = "Floorp"


class IsYesOrNo(str, Enum):
    YES = "✔️ Да"
    NO = "❌ Нет"


class WebConfig(BaseModel):
    """
    Pydantic модель для обработки сетевых данных, связанных с конфигурацией проекта.
    """

    browser: Browser = Browser.FLOORP
    bookmarks_folder: str | None = None
    custom_profile: str | None = None
    custom_report_file: str | None = None
    is_default: IsYesOrNo | bool = IsYesOrNo.NO

    @classmethod
    async def web_config_form(
        cls,
        is_default: Annotated[
            IsYesOrNo,
            Form(
                alias = "📜 Установить значения по умолчанию", 
                examples = [IsYesOrNo.NO]
            )
        ],
        browser: Annotated[
            Browser, 
            Form(
                alias = "🌎 Браузер", 
                examples = [Browser.FLOORP]
            )
        ],
        bookmarks_folder: Annotated[
            str, 
            Form(
                alias = "🏙️ Директория закладок", 
                examples = [""]
                
            )
        ] = None,
        custom_profile: Annotated[
            str, 
            Form(
                alias = "🪪 Кастомный профиль браузера", 
                examples = [""]
                
            )
        ] = None,
        custom_report_file: Annotated[
            str, Form(
                alias = "📁 Название файла репорта", 
                examples = [""]
            )
        ] = None
    ):
        return cls(
            browser = browser, 
            bookmarks_folder = bookmarks_folder, 
            custom_profile = custom_profile, 
            custom_report_file = custom_report_file,
            is_default = is_default
        )


@web.put(
    '/config', 
    description = "Задает конфигурацию для утилиты анализа закладок браузера.",
    tags = ["⚙️ Конфигурация"], 
    summary = "Задать конфигурацию"
)
async def put_config(
    web_config: Annotated[
        WebConfig, 
        Depends(WebConfig.web_config_form)
    ]
) -> dict[str, object]:
    """
    Задает конфигурацию для утилиты анализа закладок браузера.
    """

    global cfg
    if web_config.is_default == IsYesOrNo.YES:
        cfg = copy(Config())
        web_config = WebConfig()
        web_config.is_default = True
    else:
        web_config.is_default = False
        if web_config.browser:
            cfg.browser = web_config.browser
        if web_config.bookmarks_folder:
            cfg.bookmarks_folder = web_config.bookmarks_folder
        cfg.custom_profile = web_config.custom_profile
        if web_config.custom_report_file:
            cfg.custom_report_file = web_config.custom_report_file
        cfg.update_config()
    return web_config.model_dump()


@web.get(
    '/bookmarks-report', 
    description = "Возвращает отчет по анализу закладок браузера.", 
    tags = ["📊 Анализ закладок"], 
    summary = "Получить отчёт по анализу директории закладок"
)
async def get_report(
    is_web_save_file: Annotated[
        IsYesOrNo, 
        Query(
            alias = "💾 Сохранить файл", 
            examples = [IsYesOrNo.YES],
        )
    ],
    bookmarks_folder: Annotated[
        str, 
        Query(
            alias = "🏙️ Директория закладок", 
            examples = [None], 
        )
    ] = None
) -> Response:
    """
    Возвращает отчет по анализу закладок браузера.
    """

    is_save_file: bool
    err_status_code: int = 400
    is_save_file = is_web_save_file == IsYesOrNo.YES
    copy_cfg = copy(cfg)

    if bookmarks_folder:
        copy_cfg.bookmarks_folder = bookmarks_folder
        copy_cfg.custom_report_file = None
        copy_cfg.update_config()
    bookmarks_report, report_path, err = await save_bookmarks_report(is_save_file, copy_cfg)
    if err is not None:
        if err == "По указанному пути отсутствует файл базы данных закладок.":
            err += " Укажите корректный профиль браузера."
            err_status_code = 404
        return PlainTextResponse(
            content = err,
            status_code = err_status_code
        )
    if is_save_file:
        return FileResponse(
            path = report_path,
            filename = report_path.name,
            media_type = "text/plain"
        )
    return PlainTextResponse(content=bookmarks_report)


@web.post(
    '/clear-report-folder',
    description = "Безопасно очищает папку для отчетов от файлов.",
    tags = ["⚙️ Конфигурация"],
    summary = "Очистить от файлов директорию для формирования отчётов"
)
async def clear_report_folder() -> dict:
    """
    Безопасно очищает папку от файлов.
    Возвращает сводку по успешным удалениям и ошибкам.
    """
    return await clear_report_files(cfg=cfg)


def web_start() -> None:
    uvicorn_run("web.router:web", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    web_start()