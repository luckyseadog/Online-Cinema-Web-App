import json
import time
from typing import Annotated, Union

from fastapi import Cookie, Depends, HTTPException, status

from core.config import settings
from db.redis_db import RedisTokenStorage, get_redis
from schemas.entity import AccessTokenData, RefreshTokenData
from services.token_service import access_token_service, refresh_token_service


async def validate_access_token(access_token, redis: RedisTokenStorage):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No access token',
        )

    if not access_token_service.validate_token(access_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid access token',
        )

    payload_str = access_token_service.decode_b64(access_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_banned_atoken(payload['sub'], access_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is banned',
        )

    if payload['exp'] < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is expired',
        )

    if payload['iat'] < await redis.get_user_last_logout_all(payload['sub']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is withdrawn',
        )

    return payload


async def validate_refresh_token(refresh_token, redis: RedisTokenStorage):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No refresh token',
        )

    if not refresh_token_service.validate_token(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid refresh token',
        )

    payload_str = refresh_token_service.decode_b64(refresh_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_valid_rtoken(payload['sub'], refresh_token) is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=' Refresh token is not valid',
        )

    if payload['exp'] < time.time():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Refresh token is expired',
        )

    return payload


async def get_token_payload_access(
        access_token: Annotated[Union[str, None], Cookie()] = None,
        redis: RedisTokenStorage = Depends(get_redis),
) -> AccessTokenData:
    try:
        payload = await validate_access_token(access_token, redis)
    except HTTPException as e:
        raise e

    return AccessTokenData(**payload)

async def get_token_payload_refresh(
        refresh_token: Annotated[Union[str, None], Cookie()] = None,
        redis: RedisTokenStorage = Depends(get_redis),
) -> RefreshTokenData:
    try:
        payload = await validate_refresh_token(refresh_token, redis)
    except HTTPException as e:
        raise e

    return RefreshTokenData(**payload)


async def check_admin_or_super_admin_role_from_access_token(
        payload: Annotated[AccessTokenData, Depends(get_token_payload_access)] = None,
) -> list[str]:
    if not (settings.role_admin in payload.roles or settings.role_super_admin in payload.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return payload
