from uuid import UUID
from db.postgres import AsyncSession
from sqlalchemy import select, update, delete
from models.entity import RoleModel
from fastapi import Depends
from db.postgres import get_session
from schemas.entity import Role
from fastapi.encoders import jsonable_encoder


class RoleService():
    async def create_role(self, role_create: Role, db: AsyncSession = Depends(get_session)) -> Role:
        role_dto = jsonable_encoder(role_create)
        role = RoleModel(**role_dto)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def get_roles(self, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)) -> list[Role]:
        result = await db.execute(select(RoleModel))
        return [Role(
            id=role.id,
            title=role.title,
            description=role.description,
        ) for role in result.scalars().all()]

    async def get_role_by_id(self, role_id: UUID, db: AsyncSession = Depends(get_session)) -> Role:
        result = await db.execute(select(RoleModel).filter(RoleModel.id == role_id))
        return Role(
            title=result.title,
            description=result.description,
        )

    async def update_role(self, role_id: UUID, db: AsyncSession = Depends(get_session), **kwargs):
        query = (
            update(RoleModel)
            .where(RoleModel.id == role_id)
            .values(kwargs)
            .returning(RoleModel.id)
        )
        result = await db.execute(query)
        updated_role = result.fetchone()
        if updated_role is not None:
            return updated_role[0]

    async def delete_role(self, role_id: UUID, db: AsyncSession = Depends(get_session)):
        query = (
            update(RoleModel)
            .where(RoleModel.id == role_id)
            .returning(RoleModel.id)
        )
        result = await db.execute(query)
        deleted_role = result.fetchone()
        if deleted_role is not None:
            return deleted_role[0]


role_service = RoleService()