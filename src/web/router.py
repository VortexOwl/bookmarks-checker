# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from pydantic import BaseModel
from typing import Annotated, Any
from copy import copy

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.bookmarks.config import Config
from src.bookmarks.report import save_bookmarks_report

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from fastapi import FastAPI, Form, Depends, Query
from fastapi.responses import Response, FileResponse, PlainTextResponse
from uvicorn import run as uvicorn_run


web = FastAPI(
    title="📚 Bookmarks API", 
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "filter": True,
        "displayRequestDuration": True
    }
)

cfg = Config()

class WebConfig(BaseModel):
    browser: str | None
    bookmarks_folder: str | None
    custom_profile: str | None
    custom_report_file: str | None

    @classmethod
    def as_form(
        cls,
        browser: Annotated[
            str, Form(
                alias="🌎 Браузер", 
                examples=[""], nullable=True
            )
        ] = None,
        bookmarks_folder: Annotated[
            str, Form(
                alias="🏙️ Директория закладок", 
                examples=[""], nullable=True
            )
        ] = None,
        custom_profile: Annotated[
            str, Form(
                alias="🪪 Кастомный профиль браузера", 
                examples=[""], nullable=True
            )
        ] = None,
        custom_report_file: Annotated[
            str, Form(
                alias="📁 Название файла репорта", 
                examples=[""], nullable=True
            )
        ] = None
    ):
        return cls(
            browser=browser, 
            bookmarks_folder=bookmarks_folder, 
            custom_profile=custom_profile, 
            custom_report_file=custom_report_file
        )


@web.put(
    '/config', 
    description="Задает конфигурацию для утилиты анализа закладок браузера.",
    tags=["⚙️ Конфигурация"], 
    summary="Задать конфигурацию"
)
async def put_config(
    web_config: Annotated[
        WebConfig, 
        Depends(WebConfig.as_form)
    ]
) -> dict:
    """
    Задает конфигурацию для утилиты анализа закладок браузера.
    """

    if web_config.browser:
        cfg.browser = web_config.browser
    if web_config.bookmarks_folder:
        cfg.bookmarks_folder = web_config.bookmarks_folder
    cfg.custom_profile = web_config.custom_profile
    if web_config.custom_report_file:
        cfg.report_file = web_config.custom_report_file
    cfg.update_config()
    return web_config.model_dump()


@web.get(
    '/bookmarks_report', 
    description="Возвращает отчет по анализу закладок браузера.", 
    tags=["📊 Анализ закладок"], 
    summary="Получить отчет анализа закладок"
)
async def get_report(
    bookmarks_folder: Annotated[
        str, Query(
            alias="🏙️ Директория закладок", 
            examples=[cfg.bookmarks_folder], 
            nullable=True
        )
    ] = None, 
    is_save_file: Annotated[
        bool, Query(
            alias="💾 Сохранить файл", 
            examples=[False]
        )
    ] = False
) -> Response:
    """
    Возвращает отчет по анализу закладок браузера.
    """
    
    copy_cfg = copy(cfg)

    if bookmarks_folder:
        copy_cfg.bookmarks_folder = bookmarks_folder
        copy_cfg.update_config()
    bookmarks_report, report_path = await save_bookmarks_report(is_save_file, copy_cfg)
    if bookmarks_report is None:
        return PlainTextResponse(
            content="Указанная директория отсутствует в базе данных закладок."
        )
    if is_save_file:
        return FileResponse(
            path=report_path,
            filename=report_path.name,
            media_type="text/plain"
        )
    return PlainTextResponse(content=bookmarks_report)



def web_start() -> None:
    uvicorn_run("web.router:web", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    web_start()