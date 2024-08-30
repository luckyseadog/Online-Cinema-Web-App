from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.api.v1.models.access_control import RightModel
from src.db.postgres_db import get_session
from src.db.redis import get_redis
from src.models.alchemy_model import Right
from src.services.custom_error import AlreadyExistError, ErrorBody
from src.services.redis_service import RedisService


class RightsManagement:
    def __init__(self, redis: RedisService, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session

    async def creation_of_right(self, right: RightModel) -> str:
        stmt = select(Right.name).where(Right.name == right.name)
        try:
            (await self.session.scalars(stmt)).one()
        except NoResultFound:
            self.session.add(Right(**right.model_dump()))
            await self.session.commit()
            return f"Право с названием '{right.name}' создано"
        else:
            raise AlreadyExistError(ErrorBody(massage=f"Право с названием '{right.name}' уже существует"))

    async def deleting_right(self, right_name: str) -> str:
        stmt = select(Right).where(Right.name == right_name)
        try:
            right = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise AlreadyExistError(ErrorBody(massage=f"Право с названием '{right_name}' не существует"))
        else:
            await self.session.delete(right)
            await self.session.commit()
            return f"Право с названием '{right.name}' удалено"


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagement:
    return RightsManagement(redis, postgres)
