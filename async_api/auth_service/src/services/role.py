from uuid import UUID
from db.postgres import AsyncSession
from sqlalchemy import select, update, delete
from models.entity import Role
from fastapi import Depends
from db.postgres import get_session
from schemas.entity import RoleCreate, RoleInDB
from fastapi.encoders import jsonable_encoder


class RoleService():
    async def create_role(self, role_create: RoleCreate, db: AsyncSession = Depends(get_session)) -> RoleCreate:
        role_dto = jsonable_encoder(role_create)
        role = Role(**role_dto)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def get_roles(self, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)) -> list[RoleInDB]:
        result = await db.execute(select(Role))
        return [RoleInDB(
            id=role.id,
            title=role.title,
            description=role.description,
        ) for role in result.scalars().all()]

    async def get_role_by_id(self, role_id: UUID, db: AsyncSession = Depends(get_session)) -> RoleInDB:
        result = await db.execute(select(Role).filter(Role.id == role_id))
        return RoleInDB(
            title=result.title,
            description=result.description,
        )

    async def update_role(self, role_create: RoleCreate, db: AsyncSession = Depends(get_session)):
        query = (
            update(Role)
            .where(Role.id == role_create.role_id)
            .values(role_create)
            .returning(Role.id)
        )
        result = await db.execute(query)
        updated_role = result.fetchone()
        if updated_role is not None:
            return updated_role[0]

    async def delete_role(self, role_id: UUID, db: AsyncSession = Depends(get_session)):
        query = (
            update(Role)
            .where(Role.id == role_id)
            .returning(Role.id)
        )
        result = await db.execute(query)
        deleted_role = result.fetchone()
        if deleted_role is not None:
            return deleted_role[0]


role_service = RoleService()