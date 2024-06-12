from redis.asyncio import Redis
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
import time


ACCESS_TOKEN_BANNED = "banned_tokens"
REFRESH_TOKENS_VALID = "valid_refresh"
LAST_LOGOUT_ALL_LIST = "last_logout_all"


class RedisTokenStorage:

    def __init__(self, redis_instance: Redis):
        self._redis = redis_instance

    async def _add_token(self, redis_key: str, user_id: int, token: str) -> int:
        tokens = await self._redis.hgetall(redis_key)
        tokens[user_id].append(token)
        rows_affected = await self._redis.hset(redis_key, mapping=tokens)

        return rows_affected
    
    async def _tokens_tidy(self, redis_key: str) -> int:
        tokens = await self._redis.hgetall(redis_key)

        for user_id, user_tokens in tokens.items():
            user_tokens_tidied = []
            for token in user_tokens:
                payload_encoded = token.split(".")[1]
                payload = json.loads(urlsafe_b64decode(payload_encoded).decode("utf-8"))

                if payload["exp"] > time.time():
                    user_tokens_tidied.append(token)
            
            tokens[user_id] = user_tokens_tidied
        
        rows_affected = await self._redis.hset(redis_key, mapping=tokens)

        return rows_affected
    
    async def _check_token(self, redis_key: str, user_id: int, token: str):
        tokens = await self._redis.hgetall(redis_key)
        return token in tokens[user_id]
    
    async def add_banned_atoken(self, user_id: int, token: str) -> int:
        return await self._add_token(ACCESS_TOKEN_BANNED, user_id, token)

    async def add_valid_rtoken(self, user_id: int, token: str) -> int:
        return await self._add_token(REFRESH_TOKENS_VALID, user_id, token)
    
    async def banned_atokens_tidy(self) -> int:
        return await self._tokens_tidy(ACCESS_TOKEN_BANNED)

    async def valid_rtokens_tidy(self) -> int:
        return await self._tokens_tidy(REFRESH_TOKENS_VALID)

    async def check_banned_atoken(self, user_id: int, token: str):
        return await self._check_token(ACCESS_TOKEN_BANNED, user_id, token)

    async def check_valid_rtoken(self, user_id: int, token: str):
        return await self._check_token(REFRESH_TOKENS_VALID, user_id, token)
    
    async def get_user_last_logout_all(self, user_id):
        last_logouts = await self._redis.hgetall(LAST_LOGOUT_ALL_LIST)
        return last_logouts[user_id]

    async def bgsave(self):
        return await self._redis.bgsave()