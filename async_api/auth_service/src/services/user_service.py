import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import RoleModel, UserModel
from schemas.entity import Role, User
from schemas.entity_schemas import UserPatch
from services.password_service import password_service
from functools import lru_cache
from db.postgres_db import get_session
from fastapi import Depends


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User:
        stmt = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = stmt.scalars().one_or_none()
        if user:
            return User(
                id=user.id,
                login=user.login,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_superadmin=user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in user.roles
                ],
            )
        else:
            return None

    async def get_user_by_email(self, user_email: str) -> User | None:
        stmt = await self.db.execute(select(UserModel).where(UserModel.email == user_email))
        user = stmt.scalars().one_or_none()
        if user:
            return User(
                id=user.id,
                login=user.login,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_superadmin=user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in user.roles
                ],
            )
        else:
            return None

    async def get_user_by_login(self, user_login) -> User:
        stmt = await self.db.execute(select(UserModel).where(UserModel.login == user_login))
        user = stmt.scalars().one_or_none()
        if user:
            return User(
                id=user.id,
                login=user.login,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_superadmin=user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in user.roles
                ],
            )
        else:
            return None

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(select(UserModel).offset(skip).limit(limit))
        return [
            User(
                id=user.id,
                login=user.login,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_superadmin=user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in user.roles
                ],
            ) for user in result.scalars()
        ]

    async def create_user(self, user_create: User) -> User:
        user_create.password = password_service.compute_hash(user_create.password)
        user_dto = jsonable_encoder(user_create, exclude_none=True)

        if 'roles' in user_dto:
            new_roles = []
            for role in user_dto['roles']:
                result = await self.db.execute(select(RoleModel).where(RoleModel.title == role['title']))
                returned_role = result.scalars().one_or_none()
                if returned_role is None:
                    raise Exception
                new_roles.append(returned_role)

            user_dto['roles'] = new_roles

        user = UserModel(**user_dto)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            login=user.login,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_superadmin=user.is_superadmin,
            roles=[
                # jsonable_encoder(
                Role(
                    id=role.id,
                    title=role.title,
                    description=role.description,
                ) for role in user.roles
                #        )
            ],
        )

    async def update_user(self, user_id: int, user_patch: UserPatch):
        user_patch.password = password_service.compute_hash(user_patch.password) if user_patch.password else ''
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user_patch.model_dump(exclude_none=True))
            .returning(UserModel)
        )
        result = await self.db.execute(query)
        updated_user = result.scalars().one_or_none()
        await self.db.commit()

        if updated_user:
            return User(
                id=updated_user.id,
                login=updated_user.login,
                password=updated_user.password,
                first_name=updated_user.first_name,
                last_name=updated_user.last_name,
                email=updated_user.email,
                is_superadmin=updated_user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in updated_user.roles
                ],
            )
        else:
            return None

    async def delete_user(self, user_id: int):
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(deleted_at=datetime.datetime.utcnow())
            .returning(UserModel)
        )
        result = await self.db.execute(query)
        deleted_user = result.scalars().one_or_none()
        await self.db.commit()

        if deleted_user:
            return User(
                id=deleted_user.id,
                login=deleted_user.login,
                password=deleted_user.password,
                first_name=deleted_user.first_name,
                last_name=deleted_user.last_name,
                email=deleted_user.email,
                is_superadmin=deleted_user.is_superadmin,
                roles=[
                    Role(
                        id=role.id,
                        title=role.title,
                        description=role.description,
                    ) for role in deleted_user.roles
                ],
            )
        else:
            return None

    async def check_deleted(self, user_id: str):
        res_user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = res_user.scalars().one_or_none()

        if user.deleted_at is not None:
            return True
        else:
            return False


@lru_cache
def get_user_service(
        db: AsyncSession = Depends(get_session),
) -> UserService:
    # redis: RedisTokenStorage = Depends(get_redis)) -> UserService:
    return UserService(db)
