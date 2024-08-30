import hashlib
from functools import lru_cache

from redis.asyncio import Redis

ACCESS_TOKEN_MIN = 15
REFRESH_TOKEN_WEEKS = 2
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

ACCESS = 'access'
REFRESH = 'refresh'


class RedisTokenStorage:
    def __init__(self, redis_instance: Redis) -> None:
        self._redis = redis_instance

    def _compute_hash(self, data: str) -> str:
        data_bytes = data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()
    
    async def _add_token(self, user_id: str, token_type: str, token: str, time_to_exp: int):
        token_7ch = self._compute_hash(token)[:7]
        return await self._redis.setex(
            f'{user_id}:{token_type}:{token_7ch}',
            time_to_exp,
            token,
        )

    async def _check_token(self, user_id: str, token_type: str, token: str) -> bool:
        token_7ch = self._compute_hash(token)[:7]
        token_value = await self._redis.get(f'{user_id}:{token_type}:{token_7ch}')
        return True if token_value is not None else False
        
    async def add_banned_access(self, user_id: str, token: str):
        time_to_exp = ACCESS_TOKEN_MIN * 60
        return await self._add_token(user_id, ACCESS, token, time_to_exp)

    async def add_valid_refresh(self, user_id: str, token: str):
        time_to_exp = REFRESH_TOKEN_WEEKS * 7 * 24 * 60 * 60
        return await self._add_token(user_id, REFRESH, token, time_to_exp)

    async def check_banned_access(self, user_id: int, token: str) -> bool:
        return await self._check_token(user_id, ACCESS, token)

    async def check_valid_refresh(self, user_id: int, token: str) -> bool:
        return await self._check_token(user_id, REFRESH, token)

    async def delete_refresh(self, user_id: str, token: str) -> None:
        token_7ch = self._compute_hash(token)[:7]
        return self._redis.delete(f'{user_id}:{REFRESH}:{token_7ch}')

    async def delete_refresh_all(self, user_id: str):
        keys = await self._redis.keys(pattern=f'{user_id}:{REFRESH}:*')
        return await self._redis.delete(*keys)
    
    async def add_user_right(self, user_id: str, right: str):
        return await self._redis.set(
            f'{user_id}:{right}', 
            right,
        )
    
    async def check_user_right(self, user_id: str, right: str) -> bool:
        right = await self._redis.get(
            f'{user_id}:{right}'
        )
        return True if right is not None else False
    
    async def delete_user_right(self, user_id: str, right: str):
        return await self._redis.delete(
            f'{user_id}:{right}', 
            right,
        )

    async def bgsave(self):
        return await self._redis.bgsave()

    async def close(self):
        return await self._redis.aclose()


@lru_cache
async def get_redis() -> RedisTokenStorage:
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, ssl=False)
    return RedisTokenStorage(redis_client)