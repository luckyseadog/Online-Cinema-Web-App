from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from src.api.v1.models.access_control import ChangeRightModel, CreateRightModel, DeleteRightModel, RightModel
from src.services.authorization_verification_service import (
    AuthorizationVerificationService,
    get_authorization_verification_service,
)
from src.services.rights_management_service import RightsManagement, get_rights_management_service


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
    right: DeleteRightModel,
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
