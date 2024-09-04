from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.v1.models import (
    AccountHistoryModel,
    AccountModel,
    ActualTokensModel,
    HistoryModel,
    LoginModel,
    SecureAccountModel,
)
from core.config import JWTConfig, jwt_config
from models.alchemy_model import Action
from services.password_service import PasswordService, get_password_service
from services.redis_service import RedisService, get_redis
from services.user_service import UserService, get_user_service


router = APIRouter()
auth_dep = AuthJWTBearer()
auth_tags_metadata = {"name": "Авторизация", "description": "Авторизация в API."}


@AuthJWT.load_config
def get_config() -> JWTConfig:
    return jwt_config


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    response_description="Пользователь зарегистрирован",
    responses={status.HTTP_200_OK: {"model": AccountModel}},
    tags=["Авторизация"],
)
async def register(
    request: Request,
    data: AccountModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> SecureAccountModel:
    if await user_service.get_user(data.login):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Логин уже занят")

    user = await user_service.create_user(data)
    return SecureAccountModel(**user.__dict__)


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
async def login(
    request: Request,
    data: LoginModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ActualTokensModel:
    # Проверить введённые данные
    if not (user := await user_service.get_user(data.login)) or not password_service.check_password(
        data.password, user.password
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

    # Сгеренить новые токены
    access_token = await authorize.create_access_token(subject=str(user.id))
    refresh_token = await authorize.create_refresh_token(subject=access_token)
    # Записать рефреш-токен в Redis
    await redis.add_valid_refresh(user.id, refresh_token, access_token)
    # Записать права в Redis
    await redis.add_user_right(user.id, [right.id for right in user.rights])
    # Записать логин в БД
    await user_service.save_history(
        HistoryModel(
            user_id=user.id,
            ip_address=request.client.host,
            action=Action.LOGIN,
            browser_info=request.headers.get("user-agent"),
            system_info=request.headers.get("sec-ch-ua-platform"),
        )
    )
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
async def refresh(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ActualTokensModel:
    # Проверка токена на корректность и просрочку
    await authorize.jwt_refresh_token_required()
    # Вытащить Access токен из Refresh
    current_access_token = await authorize.get_jwt_subject()
    # Достать из Access информацию по юзеру
    try:
        # Изменить допустимую просрочку на срок годности Refresh токена
        authorize._decode_leeway = authorize._refresh_token_expires
        access_token_data = await authorize._verified_token(current_access_token)
    finally:
        # Вернуть допустимую просрочку к 0 в любом сценарии
        authorize._decode_leeway = 0

    user_id = access_token_data.get("sub")
    # Проверить Refresh на logout
    if not await redis.check_valid_refresh(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Сгенерить новые токены
    new_access_token = await authorize.create_access_token(subject=user_id)
    new_refresh_token = await authorize.create_refresh_token(subject=new_access_token)
    # Удалить старый рефреш
    await redis.delete_refresh(user_id, authorize._token)
    # Добавить новый рефреш
    await redis.add_valid_refresh(user_id, new_refresh_token, new_access_token)
    # Добавить старый аксес (как блокировка)
    await redis.add_banned_access(user_id, current_access_token, user_id)
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
async def logout(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> None:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    access_token = authorize._token
    user_id = await authorize.get_jwt_subject()
    # Достать refresh
    await authorize.jwt_refresh_token_required()
    refresh_token = authorize._token
    # Удалить рефреш из Redis
    await redis.delete_refresh(user_id, refresh_token)
    # Добавить аксес в Redis (как блокировка)
    await redis.add_banned_access(user_id, access_token, user_id)
    # Отдать ответ о выходе из системы
    await authorize.unset_jwt_cookies()


@router.get(
    "/logout_all",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def logout_all(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> None:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Удалить все рефреш из Redis и достать все Access
    all_user_access_tokens = await redis.delete_all_refresh(user_id)
    # Добавить все аксесы в Redis (как блокировка)
    for token in all_user_access_tokens:
        await redis.add_banned_access(user_id, token, user_id)

    # Отдать ответ о выходе из системы
    await authorize.unset_jwt_cookies()


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
async def update(
    request: Request,
    data: AccountModel,
    redis: Annotated[RedisService, Depends(get_redis)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> SecureAccountModel:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Обновить данные аккаунта в БД
    user = await user_service.update_user(user_id, data)
    # Отдать данные аккаунта
    return SecureAccountModel(**user.__dict__)


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
async def history(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> list[AccountHistoryModel]:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Получить историю входов в аккаунт из БД
    user_login_history = await user_service.get_user_login_history(user_id)
    # Отдать историю входов в аккаунт
    return [AccountHistoryModel(**history.__dict__) for history in user_login_history]
