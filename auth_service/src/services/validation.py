import json
import logging
import time
from typing import Annotated, Union

from core.config import settings
from db.redis_db import RedisTokenStorage, get_redis_token_storage
from fastapi import Cookie, Depends, Header, HTTPException, status
from fastapi.responses import ORJSONResponse
from schemas.entity_schemas import AccessTokenData, RefreshTokenData
from services.token_service import (AccessTokenService, RefreshTokenService,
                                    get_access_token_service,
                                    get_refresh_token_service)
from services.user_service import UserService, get_user_service


async def validate_access_token(
    user_agent: Annotated[Union[str, None], Header()] = None,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    access_token_service: AccessTokenService = Depends(get_access_token_service),
    cache: RedisTokenStorage = Depends(get_redis_token_storage),
):
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
    payload = AccessTokenData(**json.loads(payload_str))

    if await cache.check_banned_atoken(payload.sub, user_agent, access_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is banned',
        )

    if payload.exp < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is expired',
        )

    if payload.iat < await cache.get_user_last_logout_all(payload.sub, user_agent):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is withdrawn',
        )
    
    logging.warn(payload.iat)
    logging.warn(await cache.get_user_last_logout_all(payload.sub, user_agent))

    return payload


async def check_origin(origin: Annotated[str | None, Header()] = None):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    return origin


async def check_role_consistency(
    response: ORJSONResponse,
    origin: Annotated[str, Depends(check_origin)],
    user_service: UserService = Depends(get_user_service),
    access_token_service: AccessTokenService = Depends(get_access_token_service),
    payload: Annotated[AccessTokenData, Depends(validate_access_token)] = None,
):
    user = await user_service.get_user(payload.sub)

    if user.roles != payload.roles:
        roles = [role.title for role in user.roles]
        access_token, access_exp = access_token_service.generate_token(origin, user.id, roles)

        response.set_cookie(
            key=settings.access_token_name,
            value=access_token,
            httponly=True,
            expires=access_exp,
        )

        payload_str = access_token_service.decode_b64(access_token.split('.')[1])
        payload = AccessTokenData(**json.loads(payload_str))
    
    return payload

async def get_access_token(
    payload: Annotated[AccessTokenData, Depends(check_role_consistency)] = None,
) -> AccessTokenData:
    return payload


async def get_admin_access_token(
    payload: Annotated[AccessTokenData, Depends(check_role_consistency)] = None,
) -> AccessTokenData:
    if not (settings.role_admin in payload.roles or settings.role_super_admin in payload.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return payload


async def validate_refresh_token(
    user_agent: Annotated[Union[str, None], Header()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
    cache: RedisTokenStorage = Depends(get_redis_token_storage),
):
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

    if await cache.check_valid_rtoken(payload['sub'], user_agent, refresh_token) is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=' Refresh token is not valid',
        )

    if payload['exp'] < time.time():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Refresh token is expired',
        )

    return RefreshTokenData(**payload)


async def get_refresh_token(
    payload: Annotated[RefreshTokenData, Depends(validate_refresh_token)] = None,
) -> RefreshTokenData:
    return payload