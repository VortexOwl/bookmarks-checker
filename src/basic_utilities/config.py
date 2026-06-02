# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from dataclasses import dataclass


class BaseConfig:
    is_console_debug: bool = False
    is_not_active = True
