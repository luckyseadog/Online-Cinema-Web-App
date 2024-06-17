from fastapi import status, HTTPException
from db.postgres import AsyncSession, get_session
from fastapi import APIRouter, Depends
from schemas.entity import Role, History
from services.role_service import role_service
from services.history_service import history_service
from schemas.updates import RolePatch
from typing import Annotated, Union
from fastapi import Cookie, Header
from db.redis_db import RedisTokenStorage, get_redis
from uuid import UUID
from api.v1.utils import APIError, validate_access_token


router = APIRouter()


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
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action='/roles[GET]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)
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
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action='/roles[POST]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)
    return await role_service.create_role(role_create=role_create, db=db)


@router.put(
    '/roles',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление роли',
    description='',
)
async def update_role(
    role_id: UUID,
    role_patch: RolePatch,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    try:
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action='/roles[PUT]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)
    return await role_service.update_role(role_id=str(role_id), role_patch=role_patch, db=db)


@router.delete(
    '/roles',
    status_code=status.HTTP_200_OK,
    summary='Удаление роли',
    description='',
)
async def delete_role(
    role_id: UUID,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    try:
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action='/roles[delete]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)
    return await role_service.delete_role(role_id=str(role_id), db=db)
