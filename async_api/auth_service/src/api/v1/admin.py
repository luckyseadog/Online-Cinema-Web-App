from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from db.postgres_db import AsyncSession, get_session
from schemas.entity import User
from schemas.entity_schemas import AccessTokenData, UpdateUserRole
from services.validation import check_admin_or_super_admin_role_from_access_token
from services.user_service import UserService, get_user_service

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
    user_role: UpdateUserRole,
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_service=Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
) -> User:
    # TODO: check that role_id is valid

    if await user_service.check_deleted(payload.sub):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action=f'/user_role/assign?role_id={user_role.role_id}',
    #     fingerprint=user_agent,
    # )
    #
    # await history_service.make_note(note, db)
    updated_user = await user_service.assign_user_role(str(user_role.user_id), str(user_role.role_id))
    return updated_user


@router.post(
    '/user_role/revoke',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Отзыв роли у пользователя',
    description='',
)
async def revoke_role(
    user_role: UpdateUserRole,
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_service=Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
) -> User:
    # TODO: check that role_id is valid

    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action=f'/user_role/revoke?role_id={user_role.role_id}',
    #     fingerprint=user_agent,
    # )
    #
    # await history_service.make_note(note, db)
    updated_user = await user_service.revoke_user_role(str(user_role.user_id), str(user_role.role_id), db)
    return updated_user


@router.post(
    '/user_role/check',
    status_code=status.HTTP_200_OK,
    summary='Проверка наличия роли у пользователя',
    description='',
)
async def check_role(
    user_role: UpdateUserRole,
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    # ?payload=Annotated[ValidationService, Depends(get_validation_service)],
    user_service=Annotated[UserService, Depends(get_user_service)],

    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
):
    # TODO: check that role_id is valid

    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action=f'/user_role/check?role_id={user_role.role_id}',
    #     fingerprint=user_agent,
    # )
    #
    # await history_service.make_note(note, db)
    res = await user_service.check_user_role(str(user_role.role_id), str(user_role.role_id), db)
    return {'result': 'YES' if res else 'NO'}


@router.get('/user_role')
async def get_users(
    user_agent: Annotated[str | None, Header()] = None,
    # payload=Annotated[ValidationService, Depends(get_validation_service)],
    user_service=Annotated[UserService, Depends(get_user_service)],
    payload: AccessTokenData = Depends(check_admin_or_super_admin_role_from_access_token),
    db: AsyncSession = Depends(get_session),
) -> list[User]:
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action='/user_role',
    #     fingerprint=user_agent,
    # )
    # await history_service.make_note(note, db)

    users = await user_service.get_users(db)
    return users
