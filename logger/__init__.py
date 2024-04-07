"""Loggers and configuration for loggers."""

import os
import time
import logging
import asyncio
import json
from functools import wraps


import json_log_formatter
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError
from logstash_async.handler import AsynchronousLogstashHandler

from contextlib import contextmanager
from base_utils import clear_args_dicts
from config import config


def initialize_logger():
    """Initiliaze loggers."""

    global logger
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
def wrapping_logic(func, request_id, args, kwargs):
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
        packet[
            "messages"
        ] = f"Exception raised in {func.__name__}. exception: {str(e)}"
        logger.exception(json.dumps(packet))
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
