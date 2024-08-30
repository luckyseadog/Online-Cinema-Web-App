from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_, select, update

from src.api.v1.models.access_control import ChangeRightModel, CreateRightModel, DeleteRightModel, RightModel
from src.db.postgres_db import get_session
from src.db.redis import get_redis
from src.models.alchemy_model import Right
from src.services.custom_error import AlreadyExistError, ErrorBody
from src.services.redis_service import RedisService


class RightsManagement:
    def __init__(self, redis: RedisService, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session

    async def creation_of_right(self, right: CreateRightModel) -> RightModel:
        stmt = select(Right).where(Right.name == right.name)
        try:
            (await self.session.scalars(stmt)).one()
        except NoResultFound:
            right_ = Right(**right.model_dump())
            self.session.add(right_)
            await self.session.commit()
            await self.session.refresh(right_)
            return RightModel(id=right_.id, name=right_.name, description=right_.description)
        else:
            raise AlreadyExistError(ErrorBody(massage=f"Право с названием '{right.name}' уже существует"))

    async def deleting_right(self, right: DeleteRightModel) -> str:
        if not right.model_dump(exclude_none=True):
            raise AlreadyExistError(ErrorBody(massage="Недостаточно информации"))

        stmt = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise AlreadyExistError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))
        else:
            await self.session.delete(right_)
            await self.session.commit()
            return f"Право '{right.name or right.id}' удалено"

    async def change_of_right(self, right: ChangeRightModel) -> RightModel:
        if not right.model_dump(exclude_none=True):
            raise AlreadyExistError(ErrorBody(massage="Недостаточно информации"))

        stmt = (
            update(Right)
            .where(or_(Right.name == right.current_name, Right.id == right.id))
            .values(**right.model_dump(exclude_none=True, exclude={"id", "current_name"}))
            .returning(Right)
        )
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise AlreadyExistError(ErrorBody(massage=f"Право '{right.current_name or right.id}' не существует"))
        else:
            await self.session.commit()
            return RightModel(id=right_.id, name=right_.name, description=right_.description)


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagement:
    return RightsManagement(redis, postgres)
