import json
import time
from services.token_service import access_token_service, refresh_token_service
from db.redis_db import RedisTokenStorage

class APIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


async def validate_access_token(service_name, access_token, redis: RedisTokenStorage):
    if access_token is None:
        raise APIError(f'{service_name}: No access token')

    if not access_token_service.validate_token(access_token):
        raise APIError(f'{service_name}: Invalid access token')

    payload_str = access_token_service.decode_b64(access_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_banned_atoken(payload['sub'], access_token):
        raise APIError(f'{service_name}: Access token is banned')

    if payload['exp'] < time.time():
        raise APIError(f'{service_name}: Access token is expired')

    if payload['iat'] < await redis.get_user_last_logout_all(payload['sub']):
        raise APIError(f'{service_name}: Access token is withdrawn')

    return payload

async def validate_refresh_token(service_name, refresh_token, redis: RedisTokenStorage):
    if refresh_token is None:
        raise APIError(f'{service_name}: No refresh token')

    if not refresh_token_service.validate_token(refresh_token):
        raise APIError(f'{service_name}: Invalid refresh token')

    payload_str = refresh_token_service.decode_b64(refresh_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_valid_rtoken(payload['sub'], refresh_token) is False:
        raise APIError(f'{service_name}: Refresh token is not valid')

    if payload['exp'] < time.time():
        raise APIError(f'{service_name}: Refresh token is expired')

    return payload
