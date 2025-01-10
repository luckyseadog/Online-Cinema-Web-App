import json
import logging
import time
from typing import Annotated, Union

from fastapi import Cookie, Depends, Header, HTTPException, status
from src.db.redis_db import RedisTokenStorage, get_redis_token_storage
from src.schemas.entity_schemas import AccessTokenData
from src.services.token_service import (AccessTokenService,
                                        get_access_token_service)


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


async def check_roles(
    payload: Annotated[AccessTokenData, Depends(validate_access_token)] = None,
) -> bool:
    for role in ["user", "subscriber", "admin", "superadmin"]:
        if role in payload.roles:
            return True
    return False