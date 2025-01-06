from functools import lru_cache

from redis.asyncio import Redis
from src.core.config import settings


@lru_cache
def get_redis() -> Redis:
    return Redis(host=settings.redis_host, port=settings.redis_port)
