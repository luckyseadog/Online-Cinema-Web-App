from db.postgres import AsyncSession, get_session
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from models.entity import RoleModel
from schemas.entity import Role
from schemas.updates import RolePatch
from sqlalchemy import delete, select, update
import logging


class RoleService():
    async def create_role(self, role_create: Role, db: AsyncSession) -> Role:
        role_dto = jsonable_encoder(role_create, exclude_none=True)
        role = RoleModel(**role_dto)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def get_roles(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Role]:
        result = await db.execute(select(RoleModel))
        return [
            Role(
                id=role.id,
                title=role.title,
                description=role.description,
            ) for role in result.scalars()
        ]

    async def get_role_by_id(self, role_id: str, db: AsyncSession) -> Role:
        result = await db.execute(select(RoleModel).filter(RoleModel.id == role_id))
        returned_role = result.scalars().one()
        return Role(
            id=returned_role.id,
            title=returned_role.title,
            description=returned_role.description,
        )

    async def update_role(self, role_id: str, role_patch: RolePatch, db: AsyncSession) -> Role:
        logging.warn(role_patch.model_dump(exclude_none=True))
        query = (
            update(RoleModel)
            .where(RoleModel.id == str(role_id))
            .values(**role_patch.model_dump(exclude_none=True))
            .returning(RoleModel)
        )
        result = await db.execute(query)
        updated_role = result.scalars().one()
        await db.commit()

        resp = Role(id=updated_role.id, title=updated_role.title, description=updated_role.description)

        return resp

    async def delete_role(self, role_id: str, db: AsyncSession):
        result = await db.execute(delete(RoleModel).where(RoleModel.id == role_id).returning(RoleModel))
        deleted_role = result.scalars().one()
        await db.commit()

        resp = Role(id=deleted_role.id, title=deleted_role.title, description=deleted_role.description)

        return resp


role_service = RoleService()
