import asyncio
from collections.abc import Coroutine
from functools import lru_cache
from typing import Any, NoReturn

from redis.asyncio import Redis
from src.core.config import settings
from src.db.redis_db import get_redis


class TokenBucket:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self._cap = settings.capacity
        self._update_time = settings.update_time
        self._update_val = settings.update_val

    async def start_fill_bucket_process(self) -> NoReturn:
        while True:
            keys_bytes: list[bytes] = await self._redis.keys(pattern="token_bucket:*")
            keys = [key.decode("utf-8") for key in keys_bytes]
            for key in keys:
                value_bytes: bytes = await self._redis.get(key)
                value = int(value_bytes.decode("utf-8"))
                value = min(self._cap, value + self._update_val)
                await self._redis.set(key, value)

            await asyncio.sleep(self._update_time)

    async def request_permisson(self, user_id: str) -> Coroutine[Any, Any, Any | bool] | bool:
        val_bytes: bytes = await self._redis.get(f"token_bucket:{user_id}")
        if not val_bytes:
            await self._redis.set(f"token_bucket:{user_id}", self._cap)
            return self.request_permisson(user_id)

        val = int(val_bytes.decode("utf-8"))
        if val == 0:
            return False

        val -= 1
        await self._redis.set(f"token_bucket:{user_id}", val)
        return True


@lru_cache
def get_token_bucket() -> TokenBucket:
    redis = get_redis()
    return TokenBucket(redis)
