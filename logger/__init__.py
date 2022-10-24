"""Loggers and configuration for loggers."""

import logging
import functools
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError


FORMAT = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"


def initialize_logger(config):
    """Initiliaze loggers."""
    logging.basicConfig(
        filename="logger/logs/app.log",
        filemode="w",
        level=logging.DEBUG,
        format=FORMAT,
    )
    logging.info("Logging Initialized")
    logging.debug("Logging debug")
    logging.warning("Logging warning")
    logging.error("Error here")
    logging.exception("Exception here")


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request_id = None
        try:
            request_id = context["X-Request-ID"]
        except ContextDoesNotExistError as e:
            pass
        logging.info(
            f"Request {request_id} entering  function {func.__name__}"
        )
        try:
            result = func(*args, **kwargs)
            logging.info(
                f"Request {request_id} exiting function {func.__name__}"
            )
            return result
        except Exception as e:
            logging.exception(
                f"Exception  {request_id} raised in {func.__name__}. exception: {str(e)}"
            )

    return wrapper


def async_log(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request_id = None
        try:
            request_id = context["X-Request-ID"]
        except ContextDoesNotExistError as e:
            pass
        logging.info(
            f"Request {request_id} entering  function {func.__name__}"
        )
        try:
            result = await func(*args, **kwargs)
            logging.info(
                f"Request {request_id} exiting function {func.__name__}"
            )
            return result
        except Exception as e:
            logging.exception(
                f"Exception  {request_id} raised in {func.__name__}. exception: {str(e)}"
            )

    return wrapper
