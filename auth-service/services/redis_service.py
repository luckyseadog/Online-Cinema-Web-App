import pickle
from typing import Any

import backoff
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError


DEFAULT_REDIS = object()


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get(self, prefix_general: str, prefix_local: str, key: str) -> None | Any | object:
        if (data := await self.redis.get(f"{prefix_general}_{prefix_local}:{key}")) is None:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            return None

        result = pickle.loads(data)[0]  # pyright: ignore[reportUnknownArgumentType]
        return DEFAULT_REDIS if result is None else result

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def set(self, prefix_general: str, prefix_local: str, key: str, value: Any) -> None:
        await self.redis.set(  # pyright: ignore[reportUnknownMemberType]
            f"{prefix_general}_{prefix_local}:{key}",
            pickle.dumps((value,), protocol=pickle.HIGHEST_PROTOCOL),
            # configs.redis_cache_expire_in_seconds,
        )
