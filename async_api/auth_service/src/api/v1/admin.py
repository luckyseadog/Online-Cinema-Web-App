from fastapi import status, HTTPException, Header
from db.postgres import AsyncSession, get_session
from fastapi import APIRouter, Depends
from schemas.entity import User, History
from services.user_service import user_service
from services.history_service import history_service
from typing import Annotated, Union
from services.depends import get_current_active_user
from fastapi import Cookie
from db.redis_db import RedisTokenStorage, get_redis
from uuid import UUID
from api.v1.utils import APIError, validate_access_token

router = APIRouter()


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
    role_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    access_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> User:
    # TODO: check that role_id is valid
    try:
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action=f'/user_role/assign?role_id={role_id}',
        fingerprint=user_agent,
    )

    await history_service.make_note(note, db)
    updated_user = await user_service.assign_user_role(payload['sub'], str(role_id), db)
    return updated_user


@router.post(
    '/user_role/revoke',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Отзыв роли у пользователя',
    description='',
)
async def revoke_role(
    role_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    access_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> User:
    # TODO: check that role_id is valid
    try:
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action=f'/user_role/revoke?role_id={role_id}',
        fingerprint=user_agent,
    )

    await history_service.make_note(note, db)
    updated_user = await user_service.revoke_user_role(payload['sub'], str(role_id), db)
    return updated_user


@router.post(
    '/user_role/check',
    status_code=status.HTTP_200_OK,
    summary='Проверка наличия роли у пользователя',
    description='',
)
async def check_role(
    role_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    access_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    # TODO: check that role_id is valid
    try:
        payload = await validate_access_token('AdminService', access_token, redis)
    except APIError as e:
        raise HTTPException(status_code=401, detail=e.message)

    if 'admin' not in payload['roles']:
        raise APIError('No access')

    note = History(
        user_id=payload['sub'],
        action=f'/user_role/check?role_id={role_id}',
        fingerprint=user_agent,
    )

    await history_service.make_note(note, db)
    res = await user_service.check_user_role(payload['sub'], str(role_id), db)
    return {'result': 'YES' if res else 'NO'}
