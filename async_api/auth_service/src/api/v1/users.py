from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import ORJSONResponse

from core.config import settings
from schemas.entity import History, User
from schemas.entity_schemas import AccessTokenData, UserPatch
from services.auth_service import AuthService, get_auth_service
from services.history_service import HistoryService, get_history_service
from services.user_service import UserService, get_user_service
from services.validation import (check_role_consistency, get_access_token,
                                 get_admin_access_token)

router = APIRouter()


@router.get(
    path='/users',
    response_model=list[User],
    status_code=status.HTTP_200_OK,
    summary='Получение списка пользователей',
    description='Получить список пользователй из БД',
    dependencies=[Depends(get_admin_access_token)],
)
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    # user_agent: Annotated[str | None, Header()] = None,
):
    users = await user_service.get_users()
    return users


@router.put(
    path='/users',
    status_code=status.HTTP_200_OK,
    summary='Изменение пользователя пользователя',
    description='Добавление пользователя в БД',
    response_model=User,
    dependencies=[Depends(check_role_consistency)],
)
async def change_user(
    user_patch: UserPatch,
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
):
    # TODO пользователь только сам меняет какие-то данные?
    # Админ может менять данные пользователя?
    # Или сделать отдельную ручку, у которой будет своя схема с полями, которые может менять админ?
    db_user = await user_service.update_user(user_patch)
    return db_user


@router.delete(
    path='/users',
    description='Удаление пользователя',
    summary='Удаление пользователя из БД',
    response_model=User,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(get_current_active_user)]
)
async def delete_user(
    response: ORJSONResponse,
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    payload: Annotated[AccessTokenData, Depends(get_access_token)],
    # payload_admin: AccessTokenData = Depends(check_admin_or_super_admin_role_from_access_token),
):
    # TODO пользователь только сам себяю может удалить или админ тоже может?
    user_id = payload.sub
    db_user = await user_service.delete_user(user_id)
    await auth_service.logout_all_by_delete(user_id)
    response.delete_cookie(key=settings.access_token_name)
    response.delete_cookie(key=settings.refresh_token_name)

    return db_user


@router.get(
    path='/users/history',
    description='Получение истории операций пользователя',
    summary='История входа/выхода пользователя',
    response_model=list[History],
    status_code=status.HTTP_200_OK,
)
async def get_history(
    history_service: Annotated[HistoryService, Depends(get_history_service)],
    payload: AccessTokenData = Depends(get_access_token),
) -> list[History]:
    user_history = await history_service.get_last_user_notes(payload.sub)
    return user_history


@router.get(
    '/users/me',
    response_model=User,
    description='Текущий пользователь',
    summary='Информация о текущем пользователе',
    status_code=status.HTTP_200_OK,
)
async def get_me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(get_access_token),
):
    user = await user_service.get_user(payload.sub)
    return user
