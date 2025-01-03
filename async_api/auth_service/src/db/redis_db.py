import datetime
import hashlib
import time

from redis.asyncio import Redis

from core.config import settings

ACCESS_TOKEN_BANNED = 'banned_access'
REFRESH_TOKEN_VALID = 'valid_refresh'
LAST_LOGOUT_ALL = 'last_logout_all'

TOKEN_SEP = '<TOKEN_SEP>'
MIN_TIME = datetime.datetime(1971, 1, 1, 0, 0, 0).timestamp()


class RedisTokenStorage:

    def __init__(self, redis_instance: Redis):
        self._redis = redis_instance

    def _compute_hash(self, data: str):
        data_bytes = data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)

        return hash_object.hexdigest()

    
    async def _add_token(self, user_id: str, token_type: str, user_agent: str, token: str, time_to_exp: int):
        token_7ch = self._compute_hash(token)[:7]
        return await self._redis.setex(
            f'{user_id}:{token_type}:{user_agent}:{token_7ch}',
            time_to_exp,
            token,
        )

    async def _check_token(self, user_id: str, token_type: str, user_agent: str, token: str):
        token_7ch = self._compute_hash(token)[:7]
        token_value = await self._redis.get(f'{user_id}:{token_type}:{user_agent}:{token_7ch}')
        return True if token_value is not None else False
        
    async def add_banned_atoken(self, user_id: str, user_agent: str, token: str) -> int:
        time_to_exp = settings.access_token_min * 60
        return await self._add_token(user_id, ACCESS_TOKEN_BANNED, user_agent, token, time_to_exp)

    async def add_valid_rtoken(self, user_id: str, token: str, user_agent: str) -> int:
        time_to_exp = settings.access_token_min * 7 * 24 * 60 * 60
        return await self._add_token(user_id, REFRESH_TOKEN_VALID, user_agent, token, time_to_exp)

    async def check_banned_atoken(self, user_id: int, user_agent: str, token: str):
        return await self._check_token(user_id, ACCESS_TOKEN_BANNED, user_agent, token)

    async def check_valid_rtoken(self, user_id: int, user_agent: str, token: str):
        return await self._check_token(user_id, REFRESH_TOKEN_VALID, user_agent, token)

    async def set_user_last_logout_all(self, user_id: str, user_agent: str):
        return await self._redis.set(
            name=f'{user_id}:{LAST_LOGOUT_ALL}:{user_agent}',
            value=time.time()
        )
    
    async def set_user_last_logout_all_by_delete(self, user_id: str):
        return await self._redis.set(
            name=f'{user_id}:{LAST_LOGOUT_ALL}:ALL_USER_AGENT',
            value=time.time()
        )

    async def get_user_last_logout_all(self, user_id: str, user_agent: str):
        last_logout_time = await self._redis.get(f'{user_id}:{LAST_LOGOUT_ALL}:{user_agent}')
        last_deleted_time = await self._redis.get(f'{user_id}:{LAST_LOGOUT_ALL}:ALL_USER_AGENT')

        if last_logout_time is not None and last_deleted_time is not None:
            last_logout_time_int = float(last_logout_time.decode("utf-8"))
            last_deleted_time_int = float(last_deleted_time.decode("utf-8"))
            return max(last_logout_time_int, last_deleted_time_int)

        elif last_logout_time is not None:
            last_logout_time_int = float(last_logout_time.decode("utf-8"))
            return last_logout_time_int

        elif last_deleted_time is not None:
            last_deleted_time_int = float(last_deleted_time.decode("utf-8"))
            return last_deleted_time_int

        else:
            return MIN_TIME

    async def bgsave(self):
        return await self._redis.bgsave()

    async def close(self):
        return await self._redis.close()

    async def delete_refresh(self, user_id: str, token: str, user_agent: str):
        token_7ch = self._compute_hash(token)[:7]
        return await self._redis.delete(f'{user_id}:{REFRESH_TOKEN_VALID}:{user_agent}:{token_7ch}')

    async def delete_refresh_all(self, user_id: str, user_agent: str):
        keys = await self._redis.keys(pattern=f'{user_id}:{REFRESH_TOKEN_VALID}:{user_agent}:*')
        return await self._redis.delete(*keys)
    
    async def delete_refresh_all_by_delete(self, user_id: str):
        keys = await self._redis.keys(pattern=f'{user_id}:{REFRESH_TOKEN_VALID}:*')
        return await self._redis.delete(*keys)


redis_session =  RedisTokenStorage(Redis(host=settings.redis_host, port=settings.redis_port, ssl=False))

redis: RedisTokenStorage | None = None

# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis_session