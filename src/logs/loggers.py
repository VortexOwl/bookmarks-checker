# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from logging import (
    Logger as LibLogger, StreamHandler as LibStreamHandler, 
    FileHandler as LibFileHandler, Formatter as LibFormatter, 
    addLevelName as libAddLevelName, setLoggerClass as libSetLoggerClass, 
    getLogger as libGetLogger, 
    DEBUG, INFO, ERROR, WARNING, CRITICAL, getLevelNamesMapping, LogRecord
    )
from os import makedirs
from sys import stdout
from typing import Any, Optional, Dict


class SmartLogger(LibLogger):
    def __init__(self, name: str):
        super().__init__(name=name)
    
    
    def __str__(self) -> str:
        return f"Logger levels: {getLevelNamesMapping()}"


    def _prepare_extra(
        self,
        raw: bool,
        empty_console: bool,
        extra: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        if raw or empty_console: 
            if extra is None: extra = {}
            extra['raw'] = raw
            extra['empty_console'] = empty_console
        return extra



    def debug(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)
    

    def info(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def warning(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def error(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def critical(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)

    
    def fatal(
        self, 
        msg: Any, 
        *args: Any, 
        raw: bool = False,
        empty_console: bool = False,
        exc_info: Any = None, 
        stack_info: bool = False, 
        stacklevel: int = 2, 
        extra: Optional[Dict[str, Any]] = None, 
        **kwargs: Any,
    ) -> None:
        extra = self._prepare_extra(raw=raw, empty_console=empty_console, extra=extra)
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, 
                   stacklevel=stacklevel, extra=extra, **kwargs)


    def add_custom_level(
        self, 
        level_name: str, 
        level_num: int, 
        is_duplicate_level_num: bool = False, 
        filename: Optional[str] = None, 
        is_create_file_level: bool = True
    ) -> None:
        if not is_duplicate_level_num:
            levels = getLevelNamesMapping()
            if level_num in levels.values():
                raise ValueError(f"Level number {level_num} is already used")
        
        method_name = level_name.lower()
        libAddLevelName(level_num, level_name)
        
        def custom_log_method(self, message, *args, **kwargs) -> None:
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, **kwargs, stacklevel=2)

        if hasattr(SmartLogger, method_name):
            raise AttributeError(f"Method '{method_name}' already exists in Logger")

        setattr(SmartLogger, method_name, custom_log_method)

        if is_create_file_level:
            makedirs(name="logs", exist_ok=True)
            if filename is None:
                filename = f"logs/logs_{method_name}.log"
            elif "/" not in filename:
                filename = f"logs/logs_{filename}.log"
            add_handler(logger=self, level=level_num, filename=filename, exact=True)


class StreamHandler(LibStreamHandler):
    def __init__(self, stream=None) -> None:
        super().__init__(stream)
        self.normal_formatter = LibFormatter(fmt=basic_format, style="{", datefmt="%Y-%m-%d %H:%M:%S")
        self.raw_formatter = LibFormatter(fmt="{message}", style="{")

    def emit(self, record: LogRecord) -> None:
        if getattr(record, 'empty_console', False):
            return None
        
        if getattr(record, 'raw', False):
            self.formatter = self.raw_formatter
        else:
            self.formatter = self.normal_formatter
        
        super().emit(record)


def add_handler(logger: SmartLogger, level: int, filename: Optional[str] = None, exact: bool = False) -> None:
    if filename:
        handler = LibFileHandler(filename, encoding='utf-8')
        handler.setFormatter(LibFormatter(fmt=basic_format, style="{", datefmt="%Y-%m-%d %H:%M:%S"))
    else:
        handler = StreamHandler(stdout)
    handler.setLevel(level)
    if exact:
        handler.addFilter(lambda record: record.levelno == level)
    logger.addHandler(handler)


def basic_configuration(logger: SmartLogger, all_level: int = DEBUG) -> SmartLogger:
    logger.setLevel(level=all_level)
    logger.propagate = False
    
    # Console
    add_handler(logger=logger, level=all_level)

    # File
    makedirs(name='logs', exist_ok=True)
    add_handler(logger=logger, level=DEBUG, filename="logs/logs_debug.log", exact=True)
    add_handler(logger=logger, level=INFO, filename="logs/logs_info.log", exact=True)
    add_handler(logger=logger, level=WARNING, filename="logs/logs_warning.log", exact=True)
    add_handler(logger=logger, level=ERROR, filename="logs/logs_error.log", exact=True)
    add_handler(logger=logger, level=CRITICAL, filename="logs/logs_critical.log", exact=True)

    add_handler(logger=logger, level=all_level, filename="logs/logs_all_levels.log")
    return logger


def get_smart_logger(name: str = "smart_logger", all_level: int = DEBUG) -> SmartLogger:
    logger: SmartLogger = libGetLogger(name=name)
    if not logger.handlers:
        basic_configuration(logger=logger, all_level=all_level)
    return logger


libSetLoggerClass(SmartLogger)
basic_format:str = ("{asctime} | {levelname} | "
    "{filename} -> {funcName}: line {lineno} | "
    "Message: {message}")

