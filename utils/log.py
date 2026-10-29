import logging
from typing import Dict


class Log:
    __level_category: Dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self, name, level: str = "info"):
        self.__format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(self.__level_category.get(level.lower()))
        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setFormatter(self.__format)
        self.__logger.addHandler(self.__stream_handler)

    def info(self, message):
        self.__logger.info(message)

    def error(self, message):
        self.__logger.error(message)

    def critical(self, message):
        self.__logger.critical(message)

    def exception(self, message):
        self.__logger.exception(message)
