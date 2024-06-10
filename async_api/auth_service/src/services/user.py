
from fastapi import APIRouter, Depends, status, HTTPException, Query
from schemas.entity import UserCreate, UserInDB, RoleInDB
from sqlalchemy import select, update
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.entity import User, Role
from uuid import UUID


class UserService:
    async def get_user(self, user_id: int, db: AsyncSession = Depends(get_session)) -> UserInDB:
        user = await db.execute(select(User).where(User.id == user_id))
        return UserInDB(id=user.id, first_name=user.first_name, last_name=user.last_name)

    async def get_user_by_email(self, user_email, db: AsyncSession = Depends(get_session)) -> UserInDB:
        user = await db.execute(select(User).filter(User.email == user_email)).fetchone()
        return UserInDB(id=user.id, first_name=user.first_name, last_name=user.last_name)

    async def get_user_by_login(self, user_login, db: AsyncSession = Depends(get_session)) -> UserInDB:
        user = await db.execute(select(User).filter(User.login == user_login))
        return UserInDB(id=user.id, first_name=user.first_name, last_name=user.last_name)

    async def get_users(self, db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100) -> list[UserInDB]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return [UserInDB(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=[RoleInDB(
                id=role.id,
                title=role.title,
                description=role.description) for role in user.roles]
        ) for user in result.scalars().all()]

    async def create_user(self, user_create: UserCreate, db: AsyncSession = Depends(get_session)) -> UserInDB:
        user_dto = jsonable_encoder(user_create)
        user = User(**user_dto)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_user(self, user_id: int, db: AsyncSession = Depends(get_session), **kwargs):
        query = (
            update(User)
            .where(User.id == user_id, User.is_active == True)
            .values(kwargs)
            .returning(User.id)
        )
        result = await db.execute(query)
        update_user = result.fetchone()
        if update_user is not None:
            return update_user[0]

    async def delete_user(self, user_id: int, db: AsyncSession = Depends(get_session)):
        query = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
            .returning(User.id)
        )
        result = await db.execute(query)
        deleted_user = result.fetchone()
        if  deleted_user is not None:
            return deleted_user[0]


    async def assing_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)):

        query_user = select(User).filter(User.id == user_id)
        query_role = select(Role).filter(Role.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        user.roles.append(role)
        await db.commit()
        return UserInDB(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=[RoleInDB(id=role.id, title=role.title, description=role.description)]
        )

    async def revoke_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)):
        query_user = select(User).filter(User.id == user_id)
        query_role = select(Role).filter(Role.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        if role not in user.roles:
            return {"detail": "not found for this user"}

        user.roles.remove(role)
        await db.commit()
        return UserInDB(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=[RoleInDB(
                id=role.id,
                title=role.title,
                description=role.description
            ) for role in user.roles]
        )

    async def check_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession = Depends(get_session)):
        query_user = select(User).filter(User.id == user_id)
        query_role = select(Role).filter(Role.id == role_id)

        res_user = await db.execute(query_user)
        res_role = await db.execute(query_role)
        user = res_user.scalars().one()
        role = res_role.scalars().one()

        return role in user.roles


user_service = UserService()
