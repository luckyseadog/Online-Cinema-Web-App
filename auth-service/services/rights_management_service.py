from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
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
from services.custom_error import ResponseError
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
            raise ResponseError(massage=f"Право с названием '{right.name}' уже существует")

    async def deleting_right(self, right: SearchRightModel) -> str:
        if not right.model_dump(exclude_none=True):
            raise ResponseError(massage="Недостаточно информации")

        stmt = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Право '{right.name or right.id}' не существует")
        else:
            await self.session.delete(right_)
            await self.session.commit()
            return f"Право '{right.name or right.id}' удалено"

    async def change_of_right(self, right_old: SearchRightModel, right_new: ChangeRightModel) -> RightModel:
        if not right_old.model_dump(exclude_none=True) or not right_new.model_dump(exclude_none=True):
            raise ResponseError(massage="Недостаточно информации")

        stmt = (
            update(Right)
            .where(or_(Right.name == right_old.name, Right.id == right_old.id))
            .values(**right_new.model_dump(exclude_none=True, exclude={"id", "current_name"}))
            .returning(Right)
        )
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Право '{right_old.name or right_old.id}' не существует")
        except IntegrityError:
            raise ResponseError(massage=f"Право с названием '{right_new.name}' уже существует")
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
            raise ResponseError(massage="Недостаточно информации")

        stmt_right = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Право '{right.name or right.id}' не существует")

        stmt_user = (
            select(User)
            .options(selectinload(User.rights))
            .where(or_(User.id == user.id, User.login == user.login, User.email == user.email))
        )
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Пользователь '{user.id or user.login or user.email}' не существует")

        if right_ in user_.rights:
            raise ResponseError(
                massage=(
                    f"Пользователь '{user.id or user.login or user.email}' уже имеет право '{right.name or right.id}'"
                )
            )

        user_.rights.append(right_)
        result = ResponseUserModel(
            id=user_.id,
            login=user_.login,
            first_name=user_.first_name,
            last_name=user_.last_name,
            email=user_.email,
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in user_.rights],
        )
        await self.session.commit()
        # TODO: добавление права в redis
        return result

    async def take_away_right(self, right: SearchRightModel, user: UserModel) -> ResponseUserModel:
        if not right.model_dump(exclude_none=True) or not user.model_dump(exclude_none=True):
            raise ResponseError(massage="Недостаточно информации")

        stmt_right = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Право '{right.name or right.id}' не существует")

        stmt_user = (
            select(User)
            .options(selectinload(User.rights))
            .where(or_(User.id == user.id, User.login == user.login, User.email == user.email))
        )
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(massage=f"Пользователь '{user.id or user.login or user.email}' не существует")

        try:
            user_.rights.remove(right_)
        except ValueError:
            raise ResponseError(
                massage=(
                    f"Пользователь '{user.id or user.login or user.email}' не имеет право '{right.name or right.id}'"
                )
            )

        result = ResponseUserModel(
            id=user_.id,
            login=user_.login,
            first_name=user_.first_name,
            last_name=user_.last_name,
            email=user_.email,
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in user_.rights],
        )
        await self.session.commit()
        # TODO: удаление права из redis
        return result

    async def get_rights_user(self, user_id: UUID | None, login: str | None, email: str | None) -> RightsModel:
        if user_id is None and login is None and email is None:
            raise ResponseError(massage="Недостаточно информации")

        stmt = (
            select(User)
            .options(selectinload(User.rights))
            .where(or_(User.id == user_id, User.login == login, User.email == email))
        )
        try:
            rights = (await self.session.scalars(stmt)).unique().one()
        except NoResultFound:
            raise ResponseError(massage=f"Пользователь '{user_id or login or email}' не существует")

        return RightsModel(
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in rights.rights]
        )


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagement:
    return RightsManagement(redis, postgres)
