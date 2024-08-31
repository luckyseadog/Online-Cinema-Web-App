from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_, select, update

from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)
from db.postgres_db import get_session
from db.redis import get_redis
from models.alchemy_model import Right, User
from services.custom_error import ErrorBody, ResponseError
from services.redis_service import RedisService


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
            raise ResponseError(ErrorBody(massage=f"Право с названием '{right.name}' уже существует"))

    async def deleting_right(self, right: SearchRightModel) -> str:
        if not right.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))
        else:
            await self.session.delete(right_)
            await self.session.commit()
            return f"Право '{right.name or right.id}' удалено"

    async def change_of_right(self, right: ChangeRightModel) -> RightModel:
        if not right.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt = (
            update(Right)
            .where(or_(Right.name == right.current_name, Right.id == right.id))
            .values(**right.model_dump(exclude_none=True, exclude={"id", "current_name"}))
            .returning(Right)
        )
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.current_name or right.id}' не существует"))
        else:
            await self.session.commit()
            return RightModel(id=right_.id, name=right_.name, description=right_.description)

    async def get_all_rights(self) -> RightsModel:
        return RightsModel(
            rights=[
                RightModel(id=right.id, name=right.name, description=right.description)
                for right in (await self.session.scalars(select(Right))).fetchall()
            ]
        )

    async def assign_user_right(self, right: SearchRightModel, user: UserModel) -> ResponseUserModel:
        if not right.model_dump(exclude_none=True) or not user.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt_right = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))

        stmt_user = select(User).where(or_(User.id == user.id, User.login == user.login, User.email == user.email))
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(
                ErrorBody(massage=f"Пользователь '{user.id or user.login or user.email}' не существует")
            )

        if right_ in user_.rights:
            raise ResponseError(
                ErrorBody(
                    massage=(
                        f"Пользователь '{user.id or user.login or user.email}' "
                        f"уже имеет право '{right.name or right.id}'"
                    )
                )
            )

        user_.rights.append(right_)
        stmt_rights = select(Right).where(Right.id.in_(user_.rights))
        rights = (await self.session.scalars(stmt_rights)).fetchall()
        result = ResponseUserModel(
            id=user_.id,
            login=user_.login,
            first_name=user_.first_name,
            last_name=user_.last_name,
            email=user_.email,
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in rights],
        )
        await self.session.commit()
        return result


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagement:
    return RightsManagement(redis, postgres)
