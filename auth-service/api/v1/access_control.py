from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.param_functions import Query

from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)
from services.rights_management_service import RightsManagement, get_rights_management_service


ADMIN = "admin"

router = APIRouter()

rights_tags_metadata = {"name": "Права", "description": "Управление правами."}


@router.post(
    "/creation_of_right",
    summary="Создание права",
    description="Создание права",
    response_description="Право создано",
    responses={status.HTTP_200_OK: {"model": RightModel}},
)
async def creation_of_right(
    request: Request,
    right: CreateRightModel,
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    return await rights_management_service.creation_of_right(right)


@router.delete(
    "/deleting_right", summary="Удаление права", description="Удаление права", response_description="Право удалено"
)
async def deleting_right(
    request: Request,
    right: SearchRightModel,
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> str:
    return await rights_management_service.deleting_right(right)


@router.put(
    "/change_of_right",
    summary="Изменение права",
    description="Изменение права",
    response_description="Право изменено",
    responses={status.HTTP_200_OK: {"model": RightModel}},
)
async def change_of_right(
    request: Request,
    right_old: Annotated[
        SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право для замены")
    ],
    right_new: Annotated[
        ChangeRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Новый данные права")
    ],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    return await rights_management_service.change_of_right(right_old, right_new)


@router.get(
    "/get_all_rights",
    summary="Просмотр всех прав",
    description="Просмотр всех прав",
    response_description="Список прав",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
)
async def get_all_rights(
    request: Request,
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightsModel:
    return await rights_management_service.get_all_rights()


@router.post(
    "/assign_user_right",
    summary="Назначить пользователю право",
    description="Назначить пользователю право",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
)
async def assign_user_right(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    return await rights_management_service.assign_user_right(right, user)


@router.delete(
    "/take_away_right",
    summary="Отобрать у  пользователя право",
    description="Отобрать у  пользователя право",
    response_description="Пользователь и его права",
    responses={status.HTTP_200_OK: {"model": ResponseUserModel}},
)
async def take_away_right(
    request: Request,
    right: Annotated[SearchRightModel, Body(description="Минимум одно поле должно быть заполненно", title="Право")],
    user: Annotated[UserModel, Body(description="Минимум одно поле должно быть заполненно", title="Юзер")],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    return await rights_management_service.take_away_right(right, user)


@router.get(
    "/rights_user",
    summary="Получить права пользователя",
    description="Минимум один параметр должен быть заполнен.",
    response_description="Права пользователя",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
)
async def get_rights_user(
    request: Request,
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
    user_id: Annotated[UUID | None, Query(description="Идентификатор юзера", title="Идентификатор")] = None,
    login: Annotated[str | None, Query(description="Логин юзера", title="Логин")] = None,
    email: Annotated[str | None, Query(description="Email юзера", title="Email")] = None,
) -> RightsModel:
    return await rights_management_service.get_rights_user(user_id, login, email)
