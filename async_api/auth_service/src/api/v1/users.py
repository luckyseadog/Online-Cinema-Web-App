from fastapi import APIRouter, Depends, status, HTTPException
from schemas.entity import User, History
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import user_service
from services.depends import get_current_user
from typing import Annotated, Union
from fastapi import Cookie, Header
from services.token_service import access_token_service
from db.redis_db import RedisTokenStorage, get_redis
import json
import time
import datetime
from services.history_service import history_service
from api.v1.errors import UserError


router = APIRouter()


async def validate_token(access_token, refresh_token, redis):
    if access_token is None and refresh_token is None:
        raise UserError('You are not logged in')

    if not access_token_service.validate_token(access_token):
        raise UserError('Invalid access token')

    payload_str = access_token_service.decode_b64(access_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_banned_atoken(payload['sub'], access_token):
        raise UserError('Access token is banned')

    if payload['exp'] < time.time():
        raise UserError('Access token expired')

    return payload


@router.delete('/')
async def delete_user(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except UserError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=payload['sub'],
        occured_at=datetime.datetime.now(),
        action='/user[delete]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    db_user = await user_service.delete_user(payload['sub'], db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user


@router.patch('/')
async def change_user(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except UserError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=payload['sub'],
        occured_at=datetime.datetime.now(),
        action='/user[patch]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    db_user = await user_service.update_user(payload['sub'], db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user

@router.get('/access')
async def get_access(db: AsyncSession = Depends(get_session)):
    return {'message': 'get new tokens'}


@router.get('/history')
async def get_history(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> list[History]:
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except UserError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=payload['sub'],
        occured_at=datetime.datetime.now(),
        action='/user/history',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    user_history = await history_service.get_last_user_notes(payload['sub'])
    return user_history

@router.get('/users')
async def get_users(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> list[User]:
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except UserError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=payload['sub'],
        occured_at=datetime.datetime.now(),
        action='/user/users',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    users = await user_service.get_users(db)
    return users

@router.get('/me')
async def get_me(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except UserError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=payload['sub'],
        occured_at=datetime.datetime.now(),
        action='/user/me',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    user = await get_current_user(access_token)
    return user
