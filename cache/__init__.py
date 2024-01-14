"""Modules that contains cache related functions."""

from typing import Optional

from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
import redis.asyncio as redis


from config import config
from base_utils import clear_args_dicts


def get_redis_async_client():
    """Create and returns an asyunc redis client"""

    return redis.from_url(
        config.redis_url, encoding="utf8", decode_responses=True
    )


def initialize_cache():
    """Initialize cache with an available backend."""
    cache_backend = InMemoryBackend
    cache_source = None

    if getattr(config, "redis_url") is not None and config.env != "dev":
        cache_backend = RedisBackend
        cache_source = redis.from_url(
            config.redis_url,
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(cache_backend(cache_source), prefix="fastapi-cache")
        return None

    FastAPICache.init(cache_backend(), prefix="fastapi-cache")
    return None


def my_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    """! Key builder for cache.

    @param func (function):function to be cached
    @param namespace (Optional[str], optional): _description_. Defaults to "".
    @param request (Request, optional): Request object. Defaults to None.
    @param response (Response, optional): Response Object. Defaults to None.

    @returns (str): cache key
    """
    prefix = FastAPICache.get_prefix()
    new_args, _ = clear_args_dicts()

    cache_key = (
        f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{new_args}"
    )
    return cache_key


def testproof_cache(*cache_args, **cache_kargs):
    """Test proof cache to avoid cache when testing."""

    def inner(func):
        def wrapper(*args, **kwargs):
            if config.env in ["dev", "circle"]:
                return func(*args, **kwargs)

            result = cache(*cache_args, **cache_kargs)(func)(*args, **kwargs)

            return result

        return wrapper

    return inner
