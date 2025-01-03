from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status

from schemas.entity import Role
from services.role_service import RoleService, get_role_service
from services.validation import get_admin_access_token

router = APIRouter(
    dependencies=[Depends(get_admin_access_token)],
)


@router.get(
    '/roles',
    response_model=list[Role],
    status_code=status.HTTP_200_OK,
    summary='Get List of Roles',
    description='',
)
async def get_roles(
    role_service: Annotated[RoleService, Depends(get_role_service)],
    user_agent: Annotated[str | None, Header()] = None,
) -> list[Role]:
    return await role_service.get_roles()


@router.post(
    '/roles',
    response_model=Role,
    status_code=status.HTTP_200_OK,
    summary='Add Role',
    description='',
)
async def add_role(
    role_create: Role,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    user_agent: Annotated[str | None, Header()] = None,
):
    return await role_service.create_role(role_create=role_create)


@router.put(
    '/roles',
    response_model=Role,
    status_code=status.HTTP_200_OK,
    summary='Update Role',
    description='',
)
async def update_role(
    role_patch: Role,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    # user_agent: Annotated[str | None, Header()] = None,
) -> Role:
    return await role_service.update_role(role_patch)


@router.delete(
    '/roles',
    status_code=status.HTTP_200_OK,
    summary='Delete Role',
    description='',
)
async def delete_role(
    role_id: UUID,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    # user_agent: Annotated[str | None, Header()] = None,
):
    return await role_service.delete_role(role_id=str(role_id))
