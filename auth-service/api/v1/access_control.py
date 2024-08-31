from typing import Annotated

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
from services.authorization_verification_service import (
    AuthorizationVerificationService,
    get_authorization_verification_service,
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
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
    return await rights_management_service.creation_of_right(right)


@router.delete(
    "/deleting_right", summary="Удаление права", description="Удаление права", response_description="Право удалено"
)
async def deleting_right(
    request: Request,
    right: SearchRightModel,
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> str:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
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
    right: ChangeRightModel,
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
    return await rights_management_service.change_of_right(right)


@router.get(
    "/get_all_rights",
    summary="Просмотр всех прав",
    description="Просмотр всех прав",
    response_description="Список прав",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
)
async def get_all_rights(
    request: Request,
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightsModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
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
    right: Annotated[SearchRightModel, Body(title="Право")],
    user: Annotated[UserModel, Body(title="Юзер")],
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
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
    right: Annotated[SearchRightModel, Body(title="Право")],
    user: Annotated[UserModel, Body(title="Юзер")],
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> ResponseUserModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
    return await rights_management_service.take_away_right(right, user)


@router.post(
    "/rights_user",
    summary="Получить права пользователя",
    description="Получить права пользователя",
    response_description="Права пользователя",
    responses={status.HTTP_200_OK: {"model": RightsModel}},
)
async def get_rights_user(
    request: Request,
    user: Annotated[UserModel, Body(title="Юзер")],
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> RightsModel:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
    return await rights_management_service.get_rights_user(user)
