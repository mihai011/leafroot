"""Modules that contains cache related functions."""


import aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from config import config


def initialize_cache():
    """Initialize cache with an available backend."""
    cache_backend = InMemoryBackend
    cache_source = None

    if getattr(config, "redis_url") is not None:
        cache_backend = RedisBackend
        cache_source = aioredis.from_url(
            config.redis_url,
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(cache_backend(cache_source), prefix="fastapi-cache")
        return None

    FastAPICache.init(cache_backend(), prefix="fastapi-cache")


def testproof_cache(*cache_args, **cache_kargs):
    """Test proof cache to avoid cache when testing."""

    def inner(function):
        def wrapper(*args, **kwargs):

            if config.env == "dev":
                return function(*args, **kwargs)

            return cache(*cache_args, **cache_kargs)(function)(*args, **kwargs)

        return wrapper

    return inner
