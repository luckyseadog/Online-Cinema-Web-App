from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status, Cookie
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from async_fastapi_jwt_auth import AuthJWT

from api.v1.models import (
    AccountModel,
    UpdateAccountModel,
    LoginModel,
    ActualTokensModel,
    AccountHistoryModel,
    HistoryModel,
)
from models.alchemy_model import Action
from services.user_service import UserService, get_user_service
from services.password_service import PasswordService, get_password_service
from services.redis_service import RedisService
from db.redis import get_redis
from core.config import jwt_config

router = APIRouter()
auth_dep = AuthJWTBearer()
auth_tags_metadata = {"name": "Авторизация", "description": "Авторизация в API."}


@AuthJWT.load_config
def get_config():
    return jwt_config


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    response_description="Пользователь зарегистрирован",
    responses={status.HTTP_200_OK: {"model": AccountModel}},
    tags=["Авторизация"],
)
async def account_register(
    request: Request,
    data: AccountModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AccountModel:
    if await user_service.get_user(data.login):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Логин уже занят")
    user = await user_service.create_user(data)
    return AccountModel(**user.__dict__)


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизация пользователя",
    response_description="Пользователь авторизован",
    responses={
        status.HTTP_200_OK: {"model": ActualTokensModel},
    },
    tags=["Авторизация"],
)
async def account_login(
    request: Request,
    data: LoginModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
    redis: Annotated[RedisService, Depends(get_redis)],  # TODO: Переписать на новый RedisStorage
    authorize: AuthJWT = Depends(auth_dep)
) -> ActualTokensModel:
    # Проверить введённые данные
    if not (user := await user_service.get_user(data.login)) or not password_service.check_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    # Сгеренить новые токены
    access_token = await authorize.create_access_token(subject=user.id.__str__())
    refresh_token = await authorize.create_refresh_token(subject=access_token)
    # Записать рефреш-токен в Redis
    await redis.set(user.id, 'refresh_token', refresh_token, access_token)  # TODO: Переписать на новый RedisStorage
    # Записать права в Redis
    await redis.set(user.id, 'rights', '', await user.awaitable_attrs.rights)  # TODO: Переписать на новый RedisStorage
    # Записать логин в БД
    history = HistoryModel(
        user_id=user.id,
        ip_address=request.client.host,
        action=Action.LOGIN,
        browser_info=request.headers.get('user-agent'),
        system_info=request.headers.get('sec-ch-ua-platform')
    )
    await user_service.save_history(history)
    # Отдать токены
    await authorize.set_access_cookies(access_token)
    await authorize.set_refresh_cookies(refresh_token)
    return ActualTokensModel(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh",
    summary="Обновление токенов",
    description="Обновление токенов",
    response_description="Токены обновлены",
    responses={
        status.HTTP_200_OK: {"model": ActualTokensModel},
    },
    tags=["Авторизация"],
)
async def token_refresh(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],  # TODO: Переписать на новый RedisStorage
    authorize: AuthJWT = Depends(auth_dep)
) -> ActualTokensModel:
    # Проверка токена на корректность и просрочку
    await authorize.jwt_refresh_token_required()
    # Вытащить Access токен из Refresh
    current_access_token = await authorize.get_jwt_subject()
    # Достать из Access информацию по юзеру
    access_token_data = await authorize._verified_token(current_access_token)
    user_id = access_token_data.get("sub")
    # Сгенерить новые токены
    new_access_token = await authorize.create_access_token(subject=user_id)
    new_refresh_token = await authorize.create_refresh_token(subject=new_access_token)
    # Удалить старый рефреш
    #await redis.delete_refresh_token(user_id, authorize._token)  # TODO: Переписать на новый RedisStorage
    # Добавить новый рефреш
    #await redis.set_refresh_token(user_id, new_refresh_token)  # TODO: Переписать на новый RedisStorage
    # Добавить старый аксес (как блокировка)
    #await redis.set_access_token(user_id, new_access_token)  # TODO: Переписать на новый RedisStorage
    # Отдать новые токены
    await authorize.set_access_cookies(new_access_token)
    await authorize.set_refresh_cookies(new_refresh_token)
    return ActualTokensModel(access_token=new_access_token, refresh_token=new_refresh_token)


@router.get(
    "/logout",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def token_logout(
    request: Request,
    authorize: AuthJWT = Depends(auth_dep)
) -> dict:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    access_token = authorize._token
    current_user = await authorize.get_jwt_subject()
    # Достать refresh
    await authorize.jwt_refresh_token_required()
    refresh_token = authorize._token
    # Удалить рефреш из Redis
    #await redis.delete_refresh_token(user_id, refresh_token)  # TODO: Переписать на новый RedisStorage
    # Добавить аксес в Redis (как блокировка)
    #await redis.set_access_token(user_id, access_token)  # TODO: Переписать на новый RedisStorage
    # Отдать ответ о выходе из системы
    await authorize.unset_jwt_cookies()
    return {"user": current_user, "token": refresh_token}


@router.get(
    "/logout_all",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def user_logout(
    request: Request,
    authorize: AuthJWT = Depends(auth_dep)
) -> None:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    # Достать все рефреш из Redis
    # Достать из рефреш аксесы
    # Удалить все рефреш из Redis
    # Добавить все аксесы в Redis (как блокировка)
    # Отдать ответ о выходе из системы
    return ...


@router.patch(
    "/update",
    summary="Обновление данных аккаунта",
    description="Обновление данных аккаунта",
    response_description="Данные аккаунта обновлены",
    responses={
        status.HTTP_200_OK: {"model": AccountModel},
    },
    tags=["Авторизация"],
)
async def account_update(
    request: Request,
    data: UpdateAccountModel,
) -> AccountModel:
    # Проверить токен на корректность и просрочку
    # Обновить данные аккаунта в БД
    # Отдать данные аккаунта
    return ...


@router.get(
    "/history",
    summary="Получение истории входов в аккаунт",
    description="Получение истории входов в аккаунт",
    response_description="История входов в аккаунт получена",
    responses={
        status.HTTP_200_OK: {"model": list[AccountHistoryModel]},
    },
    tags=["Авторизация"],
)
async def account_history(
    request: Request,
) -> list[AccountHistoryModel]:
    # Проверить токен на корректность и просрочку
    # Получить историю входов в аккаунт из БД
    # Отдать историю входов в аккаунт
    return ...
