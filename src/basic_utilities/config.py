from dataclasses import dataclass


@dataclass
class BaseConfig:
    is_console_debug: bool = True
    