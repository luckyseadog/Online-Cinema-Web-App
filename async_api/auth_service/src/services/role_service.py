import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select, update

from db.postgres_db import AsyncSession
from models.entity import RoleModel
from schemas.entity import Role
from schemas.entity_schemas import RolePatch
from functools import lru_cache
from fastapi import Depends
from db.postgres_db import get_session


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_role(self, role_create: Role) -> Role:
        role_dto = jsonable_encoder(role_create, exclude_none=True)
        role = RoleModel(**role_dto)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def get_roles(self, skip: int = 0, limit: int = 10) -> list[Role]:
        result = await self.db.execute(select(RoleModel).offset(skip).limit(limit))
        return [
            Role(
                id=role.id,
                title=role.title,
                description=role.description,
            ) for role in result.scalars()
        ]

    async def get_role_by_id(self, role_id: str) -> Role:
        result = await self.db.execute(select(RoleModel).where(RoleModel.id == role_id))
        returned_role = result.scalars().one_or_none()
        return Role(
            id=returned_role.id,
            title=returned_role.title,
            description=returned_role.description,
        )

    async def get_role_by_name(self, role_name: str) -> Role:
        result = await self.db.execute(select(RoleModel).where(RoleModel.title == role_name))
        returned_role = result.scalars().one_or_none()
        if returned_role is not None:
            return Role(
                id=returned_role.id,
                title=returned_role.title,
                description=returned_role.description,
            )
        else:
            return

    async def update_role(self, role_id: str, role_patch: RolePatch) -> Role:
        logging.warn(role_patch.model_dump(exclude_none=True))
        query = (
            update(RoleModel)
            .where(RoleModel.id == str(role_id))
            .values(**role_patch.model_dump(exclude_none=True))
            .returning(RoleModel)
        )
        result = await self.db.execute(query)
        updated_role = result.scalars().one_or_none()

        if not updated_role:
            return

        await self.db.commit()
        resp = Role(id=updated_role.id, title=updated_role.title, description=updated_role.description)
        return resp

    async def delete_role(self, role_id: str):
        result = await self.db.execute(delete(RoleModel).where(RoleModel.id == role_id).returning(RoleModel))
        deleted_role = result.scalars().one_or_none()
        if deleted_role is None:
            return

        await self.db.commit()
        resp = Role(id=deleted_role.id, title=deleted_role.title, description=deleted_role.description)
        return resp


@lru_cache
def get_role_service(
        db: AsyncSession = Depends(get_session),
) -> RoleService:
    return RoleService(db=db)
