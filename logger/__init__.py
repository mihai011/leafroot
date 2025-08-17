"""Loggers and configuration for loggers."""

import asyncio
import json
import logging
import time
from contextlib import contextmanager, suppress
from functools import wraps
from typing import Callable

import json_log_formatter
from logstash_async.handler import AsynchronousLogstashHandler
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

from base_utils import clear_args_dicts
from config import config


def initialize_logger() -> None:
    """Initiliaze loggers."""
    global logger  # noqa: PLW0603
    logstash_host = "logstash"
    logstash_port = 5044
    formatter = json_log_formatter.JSONFormatter()

    logger = logging.getLogger("async_logging")

    handler = AsynchronousLogstashHandler(
        host=logstash_host,
        port=logstash_port,
        ssl_enable=False,
        ssl_verify=False,
        transport="logstash_async.transport.BeatsTransport",
        database_path="logstash.db",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


@contextmanager
def wrapping_logic(func: Callable, request_id: str, args: list, kwargs: dict) -> None:
    """Context manager for logging context data on request."""
    new_args, new_kwargs = clear_args_dicts(args, kwargs)

    if config.env in ["circle", "dev"]:
        yield
        return

    packet = {
        "request_id": request_id,
        "function_name": func.__name__,
        "function_args": new_args,
        "function_kwargs": new_kwargs,
        "start_ts": time.time(),
        "message": None,
    }
    try:
        packet["messages"] = f"Function {func.__name__} started"
        logger.info(json.dumps(packet))
        yield
        duration = time.time() - packet["start_ts"]
        packet["end_ts"] = time.time()
        packet["function_duration"] = duration
        packet["messages"] = f"Function {func.__name__} ended"
        logger.info(json.dumps(packet))
    except Exception as e:
        packet["messages"] = f"Exception raised in {func.__name__}. exception: {str(e)}"
        logger.exception(json.dumps(packet))
        raise


def log() -> Callable:
    """Log decorator to be used in the async and sync functions and methods."""

    def inner(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: dict):  # noqa: ANN401, ANN202
            request_id = None
            result = None
            with suppress(ContextDoesNotExistError):
                request_id = context["X-Request-ID"]

            if not asyncio.iscoroutinefunction(func):
                with wrapping_logic(func, request_id, args, kwargs):
                    result = func(*args, **kwargs)

            else:

                async def wrap():  # noqa: ANN401, ANN202
                    with wrapping_logic(func, request_id, args, kwargs):
                        return await func(*args, **kwargs)

                result = wrap()

            return result

        return wrapper

    return inner
