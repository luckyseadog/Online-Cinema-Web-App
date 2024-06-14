from fastapi import status, HTTPException, Header
from db.postgres import AsyncSession, get_session
from fastapi import APIRouter, Depends
from schemas.entity import Role, User, UserRoleUUID, History
from services.role_service import role_service
from services.user_service import user_service
from services.history_service import history_service
from typing import Annotated, Union
from fastapi import Cookie
from services.token_service import access_token_service, refresh_token_service
from db.redis_db import RedisTokenStorage, get_redis
import json
import time
import datetime

router = APIRouter()


class AuthError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

async def validate_token(access_token, refresh_token, redis):
    if access_token is None and refresh_token is None:
        raise AuthError("You are not logged in")

    if not access_token_service.validate_token(access_token):
        raise AuthError("Invalid access token")
    
    if await redis.check_banned_atoken(access_token):
        raise AuthError("Invalid access token")
    
    payload_str = access_token_service.decode_b64(access_token).split(".")[1]
    payload = json.loads(payload_str)

    if payload["exp"] < time.time():
        raise AuthError("Invalid access token")
    
    if "admin" not in payload["roles"]:
        raise AuthError("You have no access")
    
    return payload


@router.post(
    '/user_role/assign',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Назначение роли пользователю',
    description='''
    В теле запроса принимает два параметра: uuid пользователя и uuid роли.
    - Если у пользователяю роль присутствует ничего не происходит.\n
    - Если у пользователя нет роли, то она добавляется.\n
    - Если нет такого пользователя возвращается ошибка 404 с описанием что такого пользователя нет.\n
    - Если нет такой роли - возвращаетс ошибка 404 с описаниме, что нет такой роли.\n
    ''',
)
async def assign_role(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ) -> User:

    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/user_role/assign",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    updated_user = await user_service.assing_user_role(payload["sub"], db)
    return updated_user


@router.post(
    '/user_role/revoke',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Отзыв роли у пользователя',
    description='',
)
async def revoke_role(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ) -> User:
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/user_role/revoke",
                   fingerprint=user_agent)
    history_service.make_note(note)
    updated_user = await user_service.revoke_user_role(payload["sub"], db)
    return updated_user


@router.post(
    '/user_role/check',
    status_code=status.HTTP_200_OK,
    summary='Проверка наличия роли у пользователя',
    description='',
)
async def check_role(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/user_role/check",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    res = await user_service.check_user_role(payload["sub"], db)
    return {'result': 'YES' if res else 'NO'}


@router.get(
    '/roles',
    response_model=list[Role],
    status_code=status.HTTP_200_OK,
    summary='Получение списка ролей',
    description='',
)
async def get_roles(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ) -> list[Role]:
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/roles[GET]",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    return await role_service.get_roles(db=db)


@router.post(
    '/roles',
    response_model=Role,
    status_code=status.HTTP_200_OK,
    summary='Добавление роли',
    description='',
)
async def add_role(
    role_create: Role,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None, 
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/roles[post]",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    return await role_service.create_role(db=db, role_create=role_create)


@router.put(
    '/roles',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление роли',
    description='',
)
async def update_role(
    role_create: Role,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/roles[put]",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    return await role_service.update_role(role_create, db=db)


@router.delete(
    '/roles',
    status_code=status.HTTP_200_OK,
    summary='Удаление роли',
    description='',
)
async def delete_role(
    id: int, 
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
    ):
    try:
        payload = await validate_token(access_token, refresh_token, redis)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.message)

    note = History(user_id=payload["sub"],
                   occured_at=datetime.datetime.now(),
                   action="/roles[delete]",
                   fingerprint=user_agent)
    await history_service.make_note(note)
    return await role_service.delete_role(db=db, role_id=id)
