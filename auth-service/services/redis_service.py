import hashlib
import pickle
from functools import lru_cache
from typing import cast

import backoff
from core.config import configs
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError


redis: Redis | None = None


class RedisService:
    def __init__(self, redis_instance: Redis) -> None:
        self._redis = redis_instance

    def _compute_hash(self, data: str) -> str:
        data_bytes = data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _add_token(self, user_id: str, token_type: str, token: str, data: str, time_to_exp: int) -> None:
        """Добавляет токен в Redis с ключем в формате '{user_id}:{token_type}:{token_hash}'"""
        token_hash = self._compute_hash(token)
        return await self._redis.setex(
            f'{user_id}:{token_type}:{token_hash}',
            time_to_exp,
            pickle.dumps((data,), protocol=pickle.HIGHEST_PROTOCOL),
        )

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _check_token(self, user_id: str, token_type: str, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:{token_type}:{token_hash}'"""
        token_hash = self._compute_hash(token)
        token_value = await self._redis.get(f'{user_id}:{token_type}:{token_hash}')
        return True if token_value is not None else False

    async def add_banned_access(self, user_id: str, token: str, data: str):
        """Добавляет в Redis запись с ключем в формате '{user_id}:access:{token_hash}'"""
        time_to_exp = configs.access_token_min * 60
        return await self._add_token(user_id, "access", token, data, time_to_exp)

    async def add_valid_refresh(self, user_id: str, token: str, data: str):
        """Добавляет в Redis запись с ключем в формате '{user_id}:refresh:{token_hash}'"""
        time_to_exp = configs.refresh_token_min * 60
        return await self._add_token(user_id, "refresh", token, data, time_to_exp)

    async def check_banned_access(self, user_id: int, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:access:{token_hash}'"""
        return await self._check_token(user_id, "access", token)

    async def check_valid_refresh(self, user_id: int, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:refresh:{token_hash}'"""
        return await self._check_token(user_id, "refresh", token)

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_refresh(self, user_id: str, token: str) -> str:
        """Удаляет из Redis запись с ключем в формате '{user_id}:refresh:{token_hash}' и возвращает её значение"""
        token_hash = self._compute_hash(token)
        deleted_token_data = pickle.loads(await self._redis.get(f'{user_id}:refresh:{token_hash}'))[0]
        await self._redis.delete(f'{user_id}:refresh:{token_hash}')
        return deleted_token_data

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_all_refresh(self, user_id: str) -> list[str]:
        """Удаляет из Redis все записи с ключем в формате '{user_id}:refresh:*' и возвращает их значения"""
        keys = await self._redis.keys(pattern=f'{user_id}:refresh:*')
        deleted_tokens_data = [pickle.loads(await self._redis.get(key))[0] for key in keys]
        if keys:
            await self._redis.delete(*keys)
        return deleted_tokens_data

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def add_user_right(self, user_id: str, data: str | list[str]):
        """Добавляет в Redis запись с ключем в формате '{user_id}:rights' или добавляет в него значение right"""
        if not data:
            return
        if not isinstance(data, list):
            data = [data]
        data = [pickle.dumps(right, protocol=pickle.HIGHEST_PROTOCOL) for right in data]
        return await self._redis.sadd(
            f'{user_id}:rights',
            *data
        )

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_user_rights(self, user_id: str) -> set[str]:
        """Возвращает все права пользователя из Redis записи с ключем в формате '{user_id}:rights'"""
        rights_bytes = await self._redis.smembers(
            f'{user_id}:rights'
        )
        rights = {pickle.loads(right) for right in rights_bytes}
        return rights

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_user_right(self, user_id: str, right: str):
        """Удаляет из зписи в Redis с ключем в формате '{user_id}:rights' значение right"""
        return await self._redis.srem(
            f'{user_id}:rights',
            pickle.dumps(right, protocol=pickle.HIGHEST_PROTOCOL),
        )

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_right(self, right: str):
        """Удаляет из всех зписей в Redis с ключем в формате '*rights*' значение right"""
        keys = await self._redis.keys(pattern='*rights*')
        for key in keys:
            await self._redis.srem(
                key,
                pickle.dumps(right, protocol=pickle.HIGHEST_PROTOCOL),
            )


@lru_cache
def get_redis() -> RedisService:
    return RedisService(cast(Redis, redis))
