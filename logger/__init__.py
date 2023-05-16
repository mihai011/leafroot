"""Loggers and configuration for loggers."""

import os
import time
import logging
import asyncio
from functools import wraps

from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError
from contextlib import contextmanager
from fastapi import HTTPException, status


FORMAT = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"


def initialize_logger():
    """Initiliaze loggers."""
    pid = os.getpid()
    logging.basicConfig(
        filename=f"logger/logs/app-{pid}.log",
        filemode="w+",
        level=logging.DEBUG,
        format=FORMAT,
    )


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
        # TODO: parse the exception and return a proper one
        raise e


def log():
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_id = None
            result = None
            try:
                request_id = context["X-Request-ID"]
            except ContextDoesNotExistError as e:
                pass

            if not asyncio.iscoroutinefunction(func):
                with wrapping_logic(func, request_id):
                    result = func(*args, **kwargs)

            else:

                async def wrap():
                    with wrapping_logic(func, request_id):
                        return await func(*args, **kwargs)

                result = wrap()

            return result

        return wrapper

    return inner
