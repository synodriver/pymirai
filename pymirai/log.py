import sys

from loguru import logger as logger_

logger = logger_


class Filter:

    def __init__(self) -> None:
        self.level = "DEBUG"

    def __call__(self, record):
        record["name"] = record["name"].split(".")[0]
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


logger.remove()
default_filter = Filter()
default_format = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}")
logger.add(sys.stdout,
           colorize=True,
           diagnose=False,
           format=default_format)
