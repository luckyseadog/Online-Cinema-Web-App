from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.v1.models import (
    AccountModel,
    UpdateAccountModel,
    LoginModel,
    ActualTokensModel,
    RefreshTokensModel,
    AccountHistoryModel,
    HistoryModel,
)
from models.alchemy_model import Action
from services.user_service import UserService, get_user_service
from services.password_service import PasswordService, get_password_service
from services.token_service import AccessTokenService, RefreshTokenService, get_access_token_service, get_refresh_token_service
from services.redis_service import RedisService
from db.redis import get_redis

router = APIRouter()
auth_tags_metadata = {"name": "Авторизация", "description": "Авторизация в API."}


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
    access_token_service: Annotated[AccessTokenService, Depends(get_access_token_service)],
    refresh_token_service: Annotated[RefreshTokenService, Depends(get_refresh_token_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
) -> ActualTokensModel:
    # Проверить введённые данные
    # Сгеренить новые токены
    # Записать логин в БД
    # Записать рефреш-токен в Redis
    # Записать права в Redis
    # Отдать токены
    if not (user := await user_service.get_user(data.login)) or not password_service.check_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    print(user.__dict__)
    access_token, _ = access_token_service.generate_token('1', '2')
    refresh_token, _ = refresh_token_service.generate_token('1', '2', access_token)
    await redis.set(user.id, 'refresh_token', refresh_token, access_token)
    await redis.set(user.id, 'rights', '', await user.awaitable_attrs.rights)
    history = HistoryModel(
        user_id=user.id,
        ip_address=request.client.host,
        action=Action.LOGIN,
        browser_info=request.headers.get('user-agent'),
        system_info=request.headers.get('sec-ch-ua-platform')
    )
    await user_service.save_history(history)
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
    data: RefreshTokensModel,
) -> ActualTokensModel:
    # Проверка токена на корректность и просрочку
    # Сгенерить новые токены
    # Удалить старый рефреш
    # Добавить новый рефреш
    # Добавить старый аксес (как блокировка)
    # Отдать новые токены
    return ...


@router.get(
    "/logout",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def token_logout(
    request: Request,
) -> None:
    # Проверить токен на корректность и просрочку
    # Удалить рефреш из Redis
    # Добавить аксес в Redis (как блокировка)
    # Отдать ответ о выходе из системы
    return ...


@router.get(
    "/logout_all",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def user_logout(
    request: Request,
) -> None:
    # Проверить токен на корректность и просрочку
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
) -> list:
    # Проверить токен на корректность и просрочку
    # Получить историю входов в аккаунт из БД
    # Отдать историю входов в аккаунт
    return [request.client, request.headers.items()]
