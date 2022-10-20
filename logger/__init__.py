"""Loggers and configuration for loggers."""

import logging


FORMAT = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"


def initialize_logger(config):
    """Initiliaze loggers."""
    logging.basicConfig(
        filename="logger/logs/app_info.log",
        filemode="a",
        level=logging.INFO,
        format=FORMAT,
    )
    logging.info("Logging Initialized")
