from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from async_fastapi_jwt_auth import AuthJWT

from services.redis import RedisStorage, get_redis
from services.rights_management_service import RightsManagement, get_rights_management_service
from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)

router = APIRouter()
auth_dep = AuthJWTBearer()
rights_tags_metadata = {"name": "Права", "description": "Управление правами."}
NOT_ADMIN = "Недостаточно прав"


@router.post(
    "/creation_of_right",
    summary="Создание права",
    description="Создание права",
    response_description="Право создано",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
async def creation_of_right(
    request: Request,
    right: CreateRightModel,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Создание права и ответ пользователю
    return await rights_management_service.create_right(right)


@router.delete(
    "/deleting_right",
    summary="Удаление права",
    description="Удаление права",
    response_description="Право удалено",
    tags=["Права"],
)
async def deleting_right(
    request: Request,
    right: SearchRightModel,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> str:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Удаление права и ответ пользователю
    return await rights_management_service.delete_right(right)


@router.put(
    "/change_of_right",
    summary="Изменение права",
    description="Изменение права",
    response_description="Право изменено",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
async def change_of_right(
    request: Request,
    right_old: Annotated[
        SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право для замены")
    ],
    right_new: Annotated[
        ChangeRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Новый данные права")
    ],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Изменение права и ответ пользователю
    return await rights_management_service.change_right(right_old, right_new)


@router.get(
    "/get_all_rights",
    summary="Просмотр всех прав",
    description="Просмотр всех прав",
    response_description="Список прав",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
async def get_all_rights(
    request: Request,
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightsModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Выгрузка всех прав и ответ пользователю
    return await rights_management_service.get_all_rights()


@router.post(
    "/assign_user_right",
    summary="Назначить пользователю право",
    description="Назначить пользователю право. Допускается ввод минимум одного идентификационного поля для права и пользователя",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
async def assign_user_right(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ResponseUserModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Назначение права и ответ пользователю
    return await rights_management_service.assign_user_right(right, user)


@router.delete(
    "/take_away_right",
    summary="Отобрать у пользователя право",
    description="Отобрать у пользователя право",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
async def take_away_right(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Отъём права и ответ пользователю
    return await rights_management_service.take_away_right(right, user)


@router.post(
    "/rights_user",
    summary="Получить права пользователя",
    description="Получить права пользователя",
    response_description="Права пользователя",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
async def get_rights_user(
    request: Request,
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    redis: Annotated[RedisStorage, Depends(get_redis)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightsModel:
    # Проверка токена
    await authorize.jwt_required()
    # Проверка наличия у пользователя прав админа
    user_rights = await redis.get_user_rights(authorize.get_jwt_subject())
    admin_right = await rights_management_service.get_admin_right()
    if admin_right.id not in user_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NOT_ADMIN)
    # Отъём права и ответ пользователю
    return await rights_management_service.get_user_rights(user)
