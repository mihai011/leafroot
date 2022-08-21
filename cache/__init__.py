import aioredis
from config import config

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

def initialize_cache():
    cache_backend = InMemoryBackend
    cache_source = None

    if "REDIS_HOST" in config:
        cache_backend = RedisBackend
        cache_source = aioredis.from_url(
            "redis://{}".format(config["REDIS_HOST"]),
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(cache_backend(cache_source), prefix="fastapi-cache")
        return

    FastAPICache.init(cache_backend(), prefix="fastapi-cache")


def testproof_cache(*cache_args, **cache_kargs):

    def inner(function):

        def wrapper(*args, **kwargs):

            if config['ENVIRONMENT'] == "dev":
                return function(*args, **kwargs)

            return cache(*cache_args, **cache_kargs)(function)(*args, **kwargs)
        
        return wrapper

    return inner