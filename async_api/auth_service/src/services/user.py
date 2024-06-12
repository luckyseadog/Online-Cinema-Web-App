
from fastapi import APIRouter, Depends, status, HTTPException, Query
from schemas.entity import User, Role
from sqlalchemy import select, update, delete
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.entity import UserModel, RoleModel
from schemas.updates import UserPatch
from uuid import UUID


class UserService:
    async def get_user(self, user_id: int, db: AsyncSession = Depends(get_session)) -> User:
        stmt = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user = stmt.scalars().one()

        return User(id=user.id, 
            login=user.login, 
            password=user.password, 
            first_name=user.first_name, 
            last_name=user.last_name,
            email=user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])

    async def get_user_by_email(self, user_email: str, db: AsyncSession = Depends(get_session)) -> User:
        stmt = await db.execute(select(UserModel).where(UserModel.email == user_email))
        user = stmt.scalars().one()

        return User(id=user.id, 
            login=user.login, 
            password=user.password, 
            first_name=user.first_name, 
            last_name=user.last_name,
            email=user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])

    async def get_user_by_login(self, user_login, db: AsyncSession = Depends(get_session)) -> User:
        stmt = await db.execute(select(UserModel).where(UserModel.login == user_login))
        user = stmt.scalars().one()

        return User(id=user.id, 
            login=user.login, 
            password=user.password, 
            first_name=user.first_name, 
            last_name=user.last_name,
            email=user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])


    async def get_users(self, db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100) -> list[User]:
        result = await db.execute(select(UserModel).offset(skip).limit(limit))
        return [User(
            id=user.id,
            login=user.login, 
            password=user.password, 
            first_name=user.first_name, 
            last_name=user.last_name,
            email=user.email,
            roles=[Role(
                id=role.id,
                title=role.title,
                description=role.description) for role in user.roles]
        ) for user in result.scalars()]

    async def create_user(self, user_create: User, db: AsyncSession = Depends(get_session)) -> User:
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
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])

    async def update_user(self, user_id: int, user_patch: UserPatch, db: AsyncSession = Depends(get_session)) -> User:
        query = (
            update(UserModel)
            .where(UserModel.id == user_id, UserModel.is_active == True)
            .values(**user_patch.model_dump(exclude_none=True))
            .returning(UserModel)
        )
        result = await db.execute(query)
        updated_user = result.scalars().one()
        await db.commit()

        return User(
            id=updated_user.id, 
            login=updated_user.login, 
            password=updated_user.password, 
            first_name=updated_user.first_name, 
            last_name=updated_user.last_name,
            email=updated_user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in updated_user.roles])
    

    async def delete_user(self, user_id: int, db: AsyncSession = Depends(get_session)) -> User:
        result = await db.execute(delete(UserModel).where(UserModel.id == user_id).returning(UserModel))
        deleted_user = result.scalars().one()
        await db.commit()

        return User(
            id=deleted_user.id, 
            login=deleted_user.login, 
            password=deleted_user.password, 
            first_name=deleted_user.first_name, 
            last_name=deleted_user.last_name,
            email=deleted_user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in deleted_user.roles])


    async def assing_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)) -> User:

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
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])

    async def revoke_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)) -> User:
        query_user = select(UserModel).where(UserModel.id == user_id)
        query_role = select(RoleModel).where(RoleModel.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        if role not in user.roles:
            return {"detail": "not found for this user"}

        user.roles.remove(role)
        await db.commit()
        return User(
            id=user.id, 
            login=user.login, 
            password=user.password, 
            first_name=user.first_name, 
            last_name=user.last_name,
            email=user.email,
            roles=[Role(id=role.id,
                        title=role.title,
                        description=role.description) for role in user.roles])

    async def check_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)):
        query_user = select(UserModel).where(UserModel.id == user_id)
        query_role = select(RoleModel).where(RoleModel.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        return role in user.roles


user_service = UserService()
