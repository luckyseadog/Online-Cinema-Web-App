from fastapi import APIRouter, Depends, status, HTTPException
from schemas.entity import User, History
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import user_service
from fastapi.responses import ORJSONResponse
from services.depends import get_current_active_user
from typing import Annotated, Union
from fastapi import Cookie, Header
from db.redis_db import RedisTokenStorage, get_redis
from services.history_service import history_service
from schemas.updates import UserPatch


router = APIRouter()


@router.delete('/')
async def delete_user(
    response: ORJSONResponse,
    current_user: Annotated[User, Depends(get_current_active_user)],
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_access_token('UsersService', access_token, redis)
    # except APIError as e:
    #     raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=current_user.id,
        action='/user[delete]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    db_user = await user_service.delete_user(current_user.id, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return db_user


@router.patch('/')
async def change_user(
    user_patch: UserPatch,
    current_user: Annotated[User, Depends(get_current_active_user)],
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_access_token('UsersService', access_token, redis)
    # except APIError as e:
    #     raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=current_user.id,
        action='/user[patch]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    db_user = await user_service.update_user(current_user.id, user_patch, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user

@router.get('/access')
async def get_access(db: AsyncSession = Depends(get_session)):
    return {'message': 'get new tokens'}


@router.get('/history')
async def get_history(
    current_user: Annotated[User, Depends(get_current_active_user)],
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> list[History]:

    # try:
    #     payload = await validate_access_token('UsersService', access_token, redis)
    # except APIError as e:
    #     raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=current_user.id,
        action='/user/history',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    user_history = await history_service.get_last_user_notes(current_user.id, db)
    return user_history

@router.get('/users')
async def get_users(
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> list[User]:
    # try:
    #     payload = await validate_access_token('UsersService', access_token, redis)
    # except APIError as e:
    #     raise HTTPException(status_code=401, detail=e.message)
    #
    note = History(
        user_id=current_user.id,
        action='/user/users',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    users = await user_service.get_users(db)
    return users

@router.get(
    '/me',
    response_model=User,
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_access_token('UsersService', access_token, redis)
    # except APIError as e:
    #     raise HTTPException(status_code=401, detail=e.message)

    note = History(
        user_id=current_user.id,
        action='/user/me',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    # user = await get_current_user(access_token, db)

    return current_user
