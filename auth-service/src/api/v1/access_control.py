from typing import Annotated

from fastapi import APIRouter, Depends, Request

from src.api.v1.models.access_control import RightModel
from src.services.authorization_verification_service import (
    AuthorizationVerificationService,
    get_authorization_verification_service,
)
from src.services.rights_management_service import RightsManagement, get_rights_management_service


router = APIRouter()

ADMIN = "admin"


@router.post(
    "/creation_of_right",
    summary="Создание права",
    description="Создание права",
    # response_description="Список найденных жанров",
    # tags=["Жанры"],
)
async def creation_of_right(
    request: Request,
    right: RightModel,
    authorization_service: Annotated[AuthorizationVerificationService, Depends(get_authorization_verification_service)],
    rights_management_service: Annotated[RightsManagement, Depends(get_rights_management_service)],
) -> str:
    await authorization_service.check(request.cookies.get("access_token"), ADMIN)
    return await rights_management_service.creation_of_right(right)
