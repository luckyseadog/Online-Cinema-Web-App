from redis.asyncio import Redis
import asyncio
from functools import lru_cache
from db.redis_db import get_redis
from core.config import middleware_config

class TokenBucket:
    def __init__(self, redis: Redis): # TODO: init from envs
        self._redis = redis
        self._cap = middleware_config.capacity
        self._update_time = middleware_config.update_time
        self._update_val = middleware_config.update_val

    async def start_fill_bucket_process(self):
        while True:
            keys_bytes: list[bytes] = await self._redis.keys(pattern=f"token_bucket:*")
            keys = [key.decode("utf-8") for key in keys_bytes]
            for key in keys:
                value_bytes: bytes = await self._redis.get(key)
                value = int(value_bytes.decode("utf-8"))
                value = min(self._cap, value + self._update_val)
                await self._redis.set(key, value)
            await asyncio.sleep(self._update_time)

    async def request_permisson(self, user_ip: str):
        val_bytes: bytes = await self._redis.get(f"token_bucket:{user_ip}")
        if not val_bytes:
            await self._redis.set(f"token_bucket:{user_ip}", self._cap)
            return self.request_permisson(user_ip)
        val = int(val_bytes.decode("utf-8"))
        if val > 0:
            val -= 1
            await self._redis.set(f"token_bucket:{user_ip}", val)
            return True
        else:
            return False
        

@lru_cache
def get_token_bucket() -> TokenBucket:
    redis = get_redis()
    return TokenBucket(redis)