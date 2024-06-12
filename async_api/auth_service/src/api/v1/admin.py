from fastapi import APIRouter
from services.role_service import role_service
from services.user_service import user_service
from schemas.entity import Role
from db.postgres import get_session
from db.postgres import AsyncSession
from fastapi import Depends
from schemas.entity import User
from schemas.updates import RolePatch
from uuid import UUID
from pydantic import BaseModel


router = APIRouter()


@router.post('/user_role/assign', response_model=User)
async def assign_role(user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)) -> User:
    updated_user = await user_service.assing_user_role(user_id, role_id, db)
    return updated_user


@router.post('/user_role/revoke', response_model=User)
async def revoke_role(user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)) -> User:
    updated_user = await user_service.revoke_user_role(user_id, role_id, db)
    return updated_user


@router.post('/user_role/check')
async def check_role(user_id: UUID, role_id: UUID, db: AsyncSession = Depends((get_session))):
    res = await user_service.check_user_role(user_id, role_id, db)
    return {"result": "YES" if res else "NO"}


@router.get('/roles', response_model=list[Role])
async def get_roles(db: AsyncSession = Depends(get_session)) -> list[Role]:
    return await role_service.get_roles(db=db)


@router.post('/roles')
async def add_role(role_create: Role, db: AsyncSession = Depends(get_session)):
    return await role_service.create_role(db=db, role_create=role_create)


@router.patch('/roles')
async def update_role(role_id: UUID, role_patch: RolePatch, db: AsyncSession = Depends(get_session)):
    return await role_service.update_role(role_id, role_patch, db=db)


@router.delete('/roles')
async def delete_role(id: int, db: AsyncSession = Depends(get_session)):
    return await role_service.delete_role(db=db, role_id=id)