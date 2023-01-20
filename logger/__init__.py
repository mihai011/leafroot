"""Loggers and configuration for loggers."""

import time
import logging
import asyncio
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError
from contextlib import contextmanager


FORMAT = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"


def initialize_logger():
    """Initiliaze loggers."""
    logging.basicConfig(
        filename="logger/logs/app.log",
        filemode="w+",
        level=logging.DEBUG,
        format=FORMAT,
        force=True,
    )
    logging.info("Logging Initialized")
    logging.debug("Logging debug")
    logging.warning("Logging warning")
    logging.error("Error here")
    logging.exception("Exception here")


@contextmanager
def wrapping_logic(func, request_id):
    try:
        start_ts = time.time()
        logging.info(
            f"Request {request_id} entering  function {func.__name__}"
        )
        yield
        dur = time.time() - start_ts
        logging.info(
            f"Request {request_id} exiting function {func.__name__} total time {dur}"
        )
    except Exception as e:
        logging.exception(
            f"Exception  {request_id} raised in {func.__name__}. exception: {str(e)}"
        )


def log(*log_args, **log_kwargs):
    def inner(func):
        def wrapper(*args, **kwargs):
            request_id = None
            try:
                request_id = context["X-Request-ID"]
            except ContextDoesNotExistError as e:
                pass

            result = None

            if not asyncio.iscoroutinefunction(func):
                with wrapping_logic(func, request_id):
                    result = func(*args, **kwargs)

            else:

                async def wrap():
                    result = None
                    with wrapping_logic(func, request_id):
                        result = await func(*args, **kwargs)
                    return result

                result = wrap()

            return result

        return wrapper

    return inner
