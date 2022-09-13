"""Loggers and configuration for loggers."""
import os

import logging
from logging import Handler


FORMATTER = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

INFO_LOGGER = None
WARN_LOGGER = None
WARNING_LOGGER = None
DEBUG_LOGGER = None
CRITICAL_LOGGER = None
FATAL_LOGGER = None
ERROR_LOGGER = None


class Logger:
    """Logger class"""

    def __init__(self, level: int, log_dir: str, filename: str):
        """Constructor for logger.
        By default a logger has a FileHandler added to it.

        Args:
            level (int): level for logging
            log_dir (str): dir for logging
            file_path (str): path for logging file
        """

        global FORMATTER
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        # filename = os.path.join(log_dir, filename)
        fh = logging.FileHandler(filename=filename, mode="a")
        fh.setFormatter(FORMATTER)
        self.logger.addHandler(fh)

    def add_handler(self, handler: Handler):
        """Adding handler to logger

        Args:
            handler (Handler): Logging habdler
        """

        self.logger.addHandler(handler)

    def log(self, message):
        """loggs message

        Args:
            message (str): message to be logged
        """
        self.logger.log(message)


def initialize_loggers(config):
    """Initiliaze loggers."""

    global INFO_LOGGER
    global WARN_LOGGER
    global WARNING_LOGGER
    global CRITICAL_LOGGER
    global DEBUG_LOGGER
    global ERROR_LOGGER

    INFO_LOGGER = Logger(logging.INFO, config.LOG_DIR, config.INFO_LOG_FILE)
    WARN_LOGGER = Logger(logging.WARN, config.LOG_DIR, config.WARN_LOG_FILE)
    WARNING_LOGGER = Logger(
        logging.WARNING, config.LOG_DIR, config.WARNING_LOG_FILE
    )
    CRITICAL_LOGGER = Logger(
        logging.CRITICAL, config.LOG_DIR, config.CRITICAL_LOG_FILE
    )
    ERROR_LOGGER = Logger(logging.ERROR, config.LOG_DIR, config.ERROR_LOG_FILE)
    DEBUG_LOGGER = Logger(logging.DEBUG, config.LOG_DIR, config.DEBUG_LOG_FILE)
