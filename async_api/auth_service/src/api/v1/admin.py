from fastapi import APIRouter
from services.role import role_service
from schemas.entity import RoleInDB, RoleCreate
from db.postgres import get_session
from db.postgres import AsyncSession
from fastapi import Depends



router = APIRouter()


@router.post('/user_role/assign')
async def assign_role():
    return {"message": "assign role of a user"}


@router.post('/user_role/revoke')
async def revoke_role():

    return {"message": "revoke role of a user"}


@router.post('/user_role/check')
async def check_role():
    return {"message": "check role of a user"}


@router.get('/roles', response_model=list[RoleInDB])
async def get_roles(db: AsyncSession = Depends(get_session)) -> list[RoleInDB]:
    return await role_service.get_roles(db=db)


@router.post('/roles')
async def add_role(role_create: RoleCreate, db: AsyncSession = Depends(get_session)):
    return await role_service.create_role(db=db, role_create=role_create)


@router.patch('/roles')
async def update_role(db: AsyncSession = Depends(get_session), **kwargs):
    return await role_service.update_role(db=db, **kwargs)


@router.delete('/roles')
async def delete_role(id: int, db: AsyncSession = Depends(get_session)):
    return await role_service.delete_role(db=db, role_id=id)