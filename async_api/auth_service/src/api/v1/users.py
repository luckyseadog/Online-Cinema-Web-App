from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.postgres_db import get_session
from schemas.entity import History, User
from schemas.entity_schemas import AccessTokenData, UserPatch
# from services.depends import get_current_user
from services.user_service import UserService, get_user_service
from services.history_service import HistoryService, get_history_service
from services.validation import validate_access_token

router = APIRouter()


@router.put('/')
async def change_user(
    user_patch: UserPatch,
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(validate_access_token),
    db: AsyncSession = Depends(get_session),
):
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action='/user[patch]',
    #     fingerprint=user_agent,
    # )
    # await history_service.make_note(note, db)

    db_user = await user_service.update_user(payload.sub, user_patch, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user


@router.delete('/')
async def delete_user(
    response: ORJSONResponse,
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(),
    db: AsyncSession = Depends(get_session),
):
    if await user_service.check_deleted(payload.sub, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action='/user[delete]',
    #     fingerprint=user_agent,
    # )
    # await history_service.make_note(note, db)

    db_user = await user_service.delete_user(payload.sub, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    response.delete_cookie(key=settings.access_token_name)
    response.delete_cookie(key=settings.refresh_token_name)

    return db_user


@router.get('/history')
async def get_history(
    user_service: Annotated[UserService, Depends(get_user_service)],
    history_service: Annotated[HistoryService, Depends(get_history_service)],
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(validate_access_token),
) -> list[History]:
    if await user_service.check_deleted(payload.sub):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action='/user/history',
    #     fingerprint=user_agent,
    # )
    # await history_service.make_note(note, db)

    user_history = await history_service.get_last_user_notes(payload.sub)
    return user_history


@router.get(
    '/me',
    response_model=User,
)
async def get_me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(validate_access_token),
):
    if await user_service.check_deleted(payload.sub):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User was deleted',
        )

    # note = History(
    #     user_id=payload.sub,
    #     action='/user/me',
    #     fingerprint=user_agent,
    # )
    # await history_service.make_note(note)

    user = await user_service.get_user(payload.sub)
    return user
