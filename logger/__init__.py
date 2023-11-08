"""Loggers and configuration for loggers."""

import os
import time
import logging
import asyncio
from functools import wraps

import json_log_formatter
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

from contextlib import contextmanager
from base_utils import clear_args_dicts
from config import config


def initialize_logger():
    """Initiliaze loggers."""

    global logger
    pid = os.getpid()
    formatter = json_log_formatter.JSONFormatter()

    json_handler = logging.FileHandler(filename=f"logger/logs/app-{pid}.jsonl")
    json_handler.setFormatter(formatter)
    logger = logging.getLogger("my_json")
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


@contextmanager
def wrapping_logic(func, request_id, args, kwargs):
    new_args, new_kwargs = clear_args_dicts(args, kwargs)

    packet = {
        "request_id": request_id,
        "function_name": func.__name__,
        "function_args": new_args,
        "function_kwargs": new_kwargs,
        "start_ts": time.time(),
    }
    try:
        logger.info(f"Function {func.__name__} started", extra=packet)
        yield
        duration = time.time() - packet["start_ts"]
        packet["end_ts"] = time.time()
        packet["function_duration"] = duration
        logger.info(f"Function {func.__name__} ended", extra=packet)
    except Exception as e:
        logger.exception(
            f"Exception raised in {func.__name__}. exception: {str(e)}",
            extra=packet,
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
                with wrapping_logic(func, request_id, args, kwargs):
                    result = func(*args, **kwargs)

            else:

                async def wrap():
                    with wrapping_logic(func, request_id, args, kwargs):
                        return await func(*args, **kwargs)

                result = wrap()

            return result

        return wrapper

    return inner
