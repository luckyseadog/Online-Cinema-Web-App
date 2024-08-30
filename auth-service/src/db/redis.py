from typing import cast

from redis.asyncio import Redis

from src.services.redis_service import RedisService


redis: Redis | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> RedisService:
    return RedisService(cast(Redis, redis))
