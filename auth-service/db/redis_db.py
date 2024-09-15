from functools import lru_cache

from core.config import configs
from redis.asyncio import Redis


@lru_cache
def get_redis() -> Redis:
    return Redis(host=configs.redis_host, port=configs.redis_port)
