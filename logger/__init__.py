"""Loggers and configuration for loggers."""

import logging


FORMAT = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"


def initialize_logger(config):
    """Initiliaze loggers."""
    logging.basicConfig(
        filename="app.log", filemode="w", level=logging.INFO, format=FORMAT
    )
    logging.info("Logging Initialized")
