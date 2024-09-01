import hashlib
from functools import lru_cache

import backoff
from core.config import configs
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError


class RedisTokenStorage:
    def __init__(self, redis_instance: Redis) -> None:
        self._redis = redis_instance

    def _compute_hash(self, data: str) -> str:
        data_bytes = data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _add_token(self, user_id: str, token_type: str, token: str, data: str, time_to_exp: int):
        token_hash = self._compute_hash(token)
        return await self._redis.setex(
            f'{user_id}:{token_type}:{token_hash}',
            time_to_exp,
            data,
        )

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _check_token(self, user_id: str, token_type: str, token: str) -> bool:
        token_hash = self._compute_hash(token)
        token_value = await self._redis.get(f'{user_id}:{token_type}:{token_hash}')
        return True if token_value is not None else False

    async def add_banned_access(self, user_id: str, token: str, data: str):
        time_to_exp = configs.access_token_min * 60
        return await self._add_token(user_id, "access", token, data, time_to_exp)

    async def add_valid_refresh(self, user_id: str, token: str, data: str):
        time_to_exp = configs.refresh_token_min * 60
        return await self._add_token(user_id, "refresh", token, data, time_to_exp)

    async def check_banned_access(self, user_id: int, token: str) -> bool:
        return await self._check_token(user_id, "access", token)

    async def check_valid_refresh(self, user_id: int, token: str) -> bool:
        return await self._check_token(user_id, "refresh", token)

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_refresh(self, user_id: str, token: str) -> None:
        token_hash = self._compute_hash(token)
        deleted_token = await self._redis.get(f'{user_id}:refresh:{token_hash}').decode("utf-8")
        self._redis.delete(f'{user_id}:refresh:{token_hash}')
        return deleted_token

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_refresh_all(self, user_id: str) -> list[str]:
        keys = await self._redis.keys(pattern=f'{user_id}:refresh:*')
        deleted_tokens = [await self._redis.get(key).decode("utf-8") for key in keys]
        if keys:
            await self._redis.delete(*keys)
        return deleted_tokens

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def add_user_right(self, user_id: str, right: str):
        return await self._redis.sadd(
            f'{user_id}',
            right,
        )
    
    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_user_rights(self, user_id: str) -> list[str]:
        rights_bytes = await self._redis.smembers(
            f'{user_id}'
        )
        rights = {right.decode("utf-8") for right in rights_bytes}
        return rights
    
    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_user_right(self, user_id: str, right: str):
        return await self._redis.srem(
            f'{user_id}', 
            right,
        )


@lru_cache
async def get_redis() -> RedisTokenStorage:
    redis_client = Redis(host=configs.redis_host, port=configs.redis_port, ssl=False)
    return RedisTokenStorage(redis_client)
