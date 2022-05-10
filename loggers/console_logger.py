import logging
import sys


class CurrencyClientLogger:

    def __init__(self):
        self.__logger = logging.getLogger("Console Logger")
        self.__logger.addHandler(logging.StreamHandler(sys.stdout))
        self.__logger.setLevel(logging.INFO)

    def set_level(self, level):
        self.__logger.setLevel(level)

    def info(self, message):
        self.__logger.info(msg=message)

    def debug(self, message):
        self.__logger.debug(msg=message)

    def warning(self, message):
        self.__logger.warning(msg=message)

    def error(self, message):
        self.__logger.error(msg=message)

    def fatal(self, message):
        self.__logger.fatal(msg=message)

    def exception(self, message):
        self.__logger.exception(msg=message)
