from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status, HTTPException

from db.postgres_db import AsyncSession, get_session
from schemas.entity import History, Role
from schemas.entity_schemas import AccessTokenData, RolePatch
from services.history_service import history_service
from services.role_service import role_service
from services.user_service import user_service
from services.validation import \
    check_admin_or_super_admin_role_from_access_token

router = APIRouter()


@router.get(
    '/roles',
    response_model=list[Role],
    status_code=status.HTTP_200_OK,
    summary='Получение списка ролей',
    description='',
)
async def get_roles(
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
) -> list[Role]:
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    note = History(
        user_id=payload.sub,
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
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
):
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    note = History(
        user_id=payload.sub,
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
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
):
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    note = History(
        user_id=payload.sub,
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
    payload: Annotated[AccessTokenData, Depends(check_admin_or_super_admin_role_from_access_token)],
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
):
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    note = History(
        user_id=payload.sub,
        action='/roles[delete]',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)
    return await role_service.delete_role(role_id=str(role_id), db=db)
