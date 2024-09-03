from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status

from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)
from services.redis_service import RedisService, get_redis
from services.rights_management_service import RightsManagementService, get_rights_management_service


router = APIRouter()
auth_dep = AuthJWTBearer()
rights_tags_metadata = {"name": "Права", "description": "Управление правами."}
NOT_ADMIN = "Недостаточно прав"


@router.post(
    "/rights/create",
    summary="Создание права",
    description="Создание права",
    response_description="Право создано",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
async def create(
    request: Request,
    right: CreateRightModel,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisService, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Создание права и ответ пользователю
    return await rights_management_service.create(right)


@router.delete(
    "/rights/delete",
    summary="Удаление права",
    description="Удаление права",
    response_description="Право удалено",
    tags=["Права"],
)
async def delete(
    request: Request,
    right: SearchRightModel,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisService, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> str:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Удаление права и ответ пользователю
    return await rights_management_service.delete(right)


@router.put(
    "/rights/update",
    summary="Изменение права",
    description="Изменение права",
    response_description="Право изменено",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
async def update(
    request: Request,
    right_old: Annotated[
        SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право для замены")
    ],
    right_new: Annotated[
        ChangeRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Новый данные права")
    ],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisService, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Изменение права и ответ пользователю
    return await rights_management_service.update(right_old, right_new)


@router.get(
    "/rights/get_all",
    summary="Просмотр всех прав",
    description="Просмотр всех прав",
    response_description="Список прав",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
async def get_all(
    request: Request,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisService, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightsModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Выгрузка всех прав и ответ пользователю
    return await rights_management_service.get_all()


@router.post(
    "/rights/assign",
    summary="Назначить пользователю право",
    description="Назначить пользователю право. Допускается ввод минимум одного идентификационного поля для права и пользователя",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
async def assign(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ResponseUserModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Назначение права и ответ пользователю
    return await rights_management_service.assign(right, user)


@router.delete(
    "/rights/take_away",
    summary="Отобрать у пользователя право",
    description="Отобрать у пользователя право",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
async def take_away(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Отъём права и ответ пользователю
    return await rights_management_service.take_away(right, user)


@router.post(
    "/rights/get_user_rights",
    summary="Получить права пользователя",
    description="Минимум один параметр должен быть заполнен.",
    response_description="Права пользователя",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
async def get_user_rights(
    request: Request,
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisService, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightsModel:
    # Проверка токена
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(user_id)
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)

    # Отъём права и ответ пользователю
    return await rights_management_service.get_user_rights(user)
