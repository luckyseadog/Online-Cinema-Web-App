from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from api.v1.models.auth import (
    AccountModel,
    HistoryModel,
)
from db.postgres_db import get_session
from db.redis import get_redis
from models.alchemy_model import User, History
from services.redis_service import RedisService
from services.password_service import get_password_service, PasswordService


class UserService:
    def __init__(self, redis: RedisService, session: AsyncSession, password: PasswordService) -> None:
        self.redis = redis
        self.session = session
        self.password = password

    async def get_user(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        result = await self.session.execute(stmt)
        result = result.scalars().first()
        print(result)
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
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def save_history(self, data: HistoryModel) -> History:
        history = History(**data.model_dump())
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history


@lru_cache
def get_user_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)], password: Annotated[PasswordService, Depends(get_password_service)],
) -> UserService:
    return UserService(redis, postgres, password)
