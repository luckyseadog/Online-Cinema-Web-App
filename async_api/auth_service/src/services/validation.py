from typing import Annotated, Union
from fastapi import Cookie, HTTPException, Depends
from db.redis_db import RedisTokenStorage, get_redis
from schemas.entity import AccessTokenData
from core.config import settings
import json
import time
from services.token_service import access_token_service, refresh_token_service
from fastapi import status


class APIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


async def validate_access_token(access_token, redis: RedisTokenStorage):
    if access_token is None:
        # raise APIError(f'{service_name}: No access token')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )

    if not access_token_service.validate_token(access_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Invalid access token')

    payload_str = access_token_service.decode_b64(access_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_banned_atoken(payload['sub'], access_token):
        # raise APIError(f'{service_name}: Access token is banned')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )

    if payload['exp'] < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Access token is expired')

    if payload['iat'] < await redis.get_user_last_logout_all(payload['sub']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Access token is withdrawn')

    return payload


async def validate_refresh_token(refresh_token, redis: RedisTokenStorage):
    if refresh_token is None:
        # raise APIError(f'{service_name}: No refresh token')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )

    if not refresh_token_service.validate_token(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Invalid refresh token')

    payload_str = refresh_token_service.decode_b64(refresh_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_valid_rtoken(payload['sub'], refresh_token) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Refresh token is not valid')

    if payload['exp'] < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )
        # raise APIError(f'{service_name}: Refresh token is expired')

    return payload


async def get_token_payload(
        access_token: Annotated[Union[str, None], Cookie()] = None,
        redis: RedisTokenStorage = Depends(get_redis),
) -> AccessTokenData:
    try:
        payload = await validate_access_token(access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    return AccessTokenData(**payload)


async def check_admin_or_super_admin_role_from_access_token(
        payload: Annotated[AccessTokenData, Depends(get_token_payload)] = None,
) -> list[str]:
    if not (settings.role_admin in payload.roles or settings.role_super_admin in payload.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return payload
