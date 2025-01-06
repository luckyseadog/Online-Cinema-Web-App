import asyncio
from collections.abc import Coroutine
from functools import lru_cache
from typing import Any, NoReturn

from redis.asyncio import Redis

from core.config import middleware_config
from services.redis_service import redis


class TokenBucket:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self._cap = middleware_config.capacity
        self._update_time = middleware_config.update_time
        self._update_val = middleware_config.update_val

    async def start_fill_bucket_process(self) -> NoReturn:
        while True:
            keys_bytes = await self._redis.keys(pattern="token_bucket:*")
            keys = [key.decode("utf-8") for key in keys_bytes]
            for key in keys:
                value_bytes: bytes = await self._redis.get(key)
                value = int(value_bytes.decode("utf-8"))
                value = min(self._cap, value + self._update_val)
                await self._redis.set(key, value)

            await asyncio.sleep(self._update_time)

    async def request_permisson(self, user_ip: str) -> Coroutine[Any, Any, Any | bool] | bool:
        val_bytes: bytes = await self._redis.get(f"token_bucket:{user_ip}")
        if not val_bytes:
            await self._redis.set(f"token_bucket:{user_ip}", self._cap)
            return self.request_permisson(user_ip)

        val = int(val_bytes.decode("utf-8"))
        if val == 0:
            return False

        val -= 1
        await self._redis.set(f"token_bucket:{user_ip}", val)
        return True


@lru_cache
def get_token_bucket() -> TokenBucket:
    return TokenBucket(redis)
