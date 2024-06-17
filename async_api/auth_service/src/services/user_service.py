from schemas.entity import User, Role
from sqlalchemy import select, update, delete
from db.postgres import get_session
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from models.entity import UserModel, RoleModel
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.updates import UserPatch
from services.password_service import password_service 


class UserService:
    async def get_user(self, user_id: int, db: AsyncSession) -> User:
        stmt = await db.execute(select(UserModel).where(UserModel.id == user_id))
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

    async def get_user_by_email(self, user_email: str, db: AsyncSession) -> User | None:
        stmt = await db.execute(select(UserModel).where(UserModel.email == user_email))
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

    async def get_user_by_login(self, user_login, db: AsyncSession) -> User:
        stmt = await db.execute(select(UserModel).where(UserModel.login == user_login))
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

    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
        result = await db.execute(select(UserModel).offset(skip).limit(limit))
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

    async def create_user(self, user_create: User, db: AsyncSession) -> User:
        user_create.password = password_service.compute_hash(user_create.password) if user_create.password else ""
        user_dto = jsonable_encoder(user_create, exclude_none=True)
        user = UserModel(**user_dto)
        db.add(user)
        await db.commit()
        await db.refresh(user)
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

    async def update_user(self, user_id: int, user_patch: UserPatch, db: AsyncSession):
        user_patch.password = password_service.compute_hash(user_patch.password) if user_patch.password else "" 
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user_patch.model_dump(exclude_none=True))
            .returning(UserModel)
        )
        result = await db.execute(query)
        updated_user = result.scalars().one_or_none()
        await db.commit()

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

    async def delete_user(self, user_id: int, db: AsyncSession):
        result = await db.execute(delete(UserModel).where(UserModel.id == user_id).returning(UserModel))
        deleted_user = result.scalars().one_or_none()
        await db.commit()

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

        

    async def assign_user_role(self, user_id: str, role_id: str, db: AsyncSession):
        query_user = select(UserModel).where(UserModel.id == user_id)
        query_role = select(RoleModel).where(RoleModel.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()


        user.roles.append(role)
        await db.commit()
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

    async def revoke_user_role(self, user_id: str, role_id: str, db: AsyncSession):
        query_user = select(UserModel).where(UserModel.id == user_id)
        query_role = select(RoleModel).where(RoleModel.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        if role not in user.roles:
            return {'detail': 'not found for this user'}

        user.roles.remove(role)
        await db.commit()
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

    async def check_user_role(self, user_id: str, role_id: str, db: AsyncSession):
        query_user = select(UserModel).filter(UserModel.id == user_id)
        query_role = select(RoleModel).filter(RoleModel.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        return role in user.roles


user_service = UserService()
