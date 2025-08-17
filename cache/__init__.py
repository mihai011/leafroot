"""Modules that contains cache related functions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from base_utils import clear_args_dicts
from config import config

if TYPE_CHECKING:
    from fastapi import Request, Response
    from redis.asyncio.client import Redis


def get_redis_async_client() -> Redis:
    """Create and returns an asyunc redis client."""
    return redis.from_url(config.redis_url, encoding="utf8", decode_responses=True)


def initialize_cache() -> None:
    """Initialize cache with an available backend."""
    cache_backend = InMemoryBackend
    cache_source = None

    if config.redis_url is not None and config.env != "dev":
        cache_backend = RedisBackend
        cache_source = redis.from_url(
            config.redis_url,
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(cache_backend(cache_source), prefix="leafroot")
        return

    FastAPICache.init(cache_backend(), prefix="leafroot")
    return


def my_key_builder(
    func: Callable,
    namespace: str | None = "",
    _request: Request = None,
    _response: Response = None,
    *_: list,
    **kwargs: dict,
) -> str:
    """! Key builder for cache.

    @param func (function):function to be cached
    @param namespace (Optional[str], optional): _description_. Defaults to "".
    @param request (Request, optional): Request object. Defaults to None.
    @param response (Response, optional): Response Object. Defaults to None.

    @returns (str): cache key
    """
    prefix = FastAPICache.get_prefix()
    new_args, new_kwargs = clear_args_dicts(kwargs["args"], kwargs["kwargs"])

    return f"""{prefix}:{namespace}:{func.__module__}:\
        {func.__name__}:{new_kwargs}:{new_args}"""


def testproof_cache(*cache_args: list, **cache_kargs: dict) -> Callable:
    """Test proof cache to avoid cache when testing."""

    def inner(func: Callable) -> Callable:
        def wrapper(*args: list, **kwargs: dict):  # noqa:ANN202
            if config.env in ["dev", "circle"]:
                return func(*args, **kwargs)

            return cache(*cache_args, **cache_kargs)(func)(*args, **kwargs)

        return wrapper

    return inner
