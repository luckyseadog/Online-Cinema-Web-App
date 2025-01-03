from typing import Annotated

from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Body, Depends, Request, status

from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)
from core.config import admin_config
from jwt_auth_helpers import rights_required
from services.rights_management_service import RightsManagementService, get_rights_management_service


router = APIRouter(prefix="/rights")
auth_dep = AuthJWTBearer()
rights_tags_metadata = {"name": "Права", "description": "Управление правами."}
NOT_ADMIN = "Недостаточно прав"


@router.post(
    "/create",
    summary="Создание права",
    description="Создание права",
    response_description="Право создано",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def create(
    request: Request,
    right: CreateRightModel,
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightModel:
    # Создание права и ответ пользователю
    return await rights_management_service.create(right)


@router.delete(
    "/delete",
    summary="Удаление права",
    description="Удаление права",
    response_description="Право удалено",
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def delete(
    request: Request,
    right: SearchRightModel,
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> str:
    # Удаление права и ответ пользователю
    return await rights_management_service.delete(right)


@router.put(
    "/update",
    summary="Изменение права",
    description="Изменение права",
    response_description="Право изменено",
    responses={status.HTTP_200_OK: {"model": RightModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def update(
    request: Request,
    right_old: Annotated[
        SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право для замены")
    ],
    right_new: Annotated[
        ChangeRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Новый данные права")
    ],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightModel:
    # Изменение права и ответ пользователю
    return await rights_management_service.update(right_old, right_new)


@router.get(
    "/get_all",
    summary="Просмотр всех прав",
    description="Просмотр всех прав",
    response_description="Список прав",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def get_all(
    request: Request,
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightsModel:
    # Выгрузка всех прав и ответ пользователю
    return await rights_management_service.get_all()


@router.post(
    "/assign",
    summary="Назначить пользователю право",
    description="Назначить пользователю право. Допускается ввод минимум одного поля для права и пользователя",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def assign(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    # Назначение права и ответ пользователю
    return await rights_management_service.assign(right, user)


@router.delete(
    "/take_away",
    summary="Отобрать у пользователя право",
    description="Отобрать у пользователя право",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def take_away(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    # Отъём права и ответ пользователю
    return await rights_management_service.take_away(right, user)


@router.post(
    "/get_user_rights",
    summary="Получить права пользователя",
    description="Минимум один параметр должен быть заполнен.",
    response_description="Права пользователя",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
    tags=["Права"],
)
@rights_required({admin_config.right_name})
async def get_user_rights(
    request: Request,
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightsModel:
    # Отъём права и ответ пользователю
    return await rights_management_service.get_user_rights(user)
