from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from api.v1.models.auth import (
    AccountModel,
    HistoryModel,
)
from db.postgres_db import get_session
from models.alchemy_model import User, History, Action
from services.password_service import get_password_service, PasswordService
from services.custom_error import ResponseError


class UserService:
    def __init__(self, session: AsyncSession, password: PasswordService) -> None:
        self.session = session
        self.password = password

    async def get_user(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        return result

    async def get_user_by_id(self, id_: str) -> User | None:
        stmt = select(User).where(User.id == id_)
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        return result

    async def create_user(self, data: AccountModel) -> User:
        user = User(**data.model_dump())
        user.password = self.password.compute_hash(user.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, data: AccountModel) -> User:
        user = await self.session.get(User, user_id)
        if user is None:
            raise NoResultFound(f"User with id '{user_id}' not found")
        for key, value in data.model_dump().items():
            if key == 'password':
                value = self.password.compute_hash(value)
            setattr(user, key, value)
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise ResponseError(e.args[0].split('DETAIL:  ')[1])
        await self.session.refresh(user)
        return user

    async def save_history(self, data: HistoryModel) -> History:
        history = History(**data.model_dump())
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_user_login_history(self, user_id: int) -> list[History]:
        stmt = select(History).where(History.user_id == user_id, History.action == Action.LOGIN)
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        return result


@lru_cache
def get_user_service(
    postgres: Annotated[AsyncSession, Depends(get_session)],
    password: Annotated[PasswordService, Depends(get_password_service)],
) -> UserService:
    return UserService(postgres, password)
