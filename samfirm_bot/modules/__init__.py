""" SamFirm Bot modules loader"""
from os.path import dirname

from samfirm_bot import TG_LOGGER
from samfirm_bot.utils.loader import get_modules

ALL_MODULES = get_modules(dirname(__file__))
TG_LOGGER.info("Modules to load: %s", str(ALL_MODULES))
# __all__ = ALL_MODULES + ["ALL_MODULES"]
