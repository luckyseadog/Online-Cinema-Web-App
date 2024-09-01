from functools import lru_cache
from typing import Annotated

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
from models.alchemy_model import RightOrm, UserOrm
from models.errors import ErrorBody
from services.custom_error import ResponseError
from services.redis_service import RedisService


class RightsManagement:
    def __init__(self, redis: RedisService, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session

    async def creation_of_right(self, right: CreateRightModel) -> RightModel:
        stmt = select(RightOrm).where(RightOrm.name == right.name)
        try:
            (await self.session.scalars(stmt)).one()
        except NoResultFound:
            right_ = RightOrm(**right.model_dump())
            self.session.add(right_)
            await self.session.commit()
            await self.session.refresh(right_)
            return RightModel(id=right_.id, name=right_.name, description=right_.description)
        else:
            raise ResponseError(ErrorBody(massage=f"Право с названием '{right.name}' уже существует"))

    async def deleting_right(self, right: SearchRightModel) -> str:
        if not right.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt = select(RightOrm).where(or_(RightOrm.name == right.name, RightOrm.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))
        else:
            await self.session.delete(right_)
            await self.session.commit()
            return f"Право '{right.name or right.id}' удалено"

    async def change_of_right(self, right_old: SearchRightModel, right_new: ChangeRightModel) -> RightModel:
        if not right_old.model_dump(exclude_none=True) or not right_new.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt = (
            update(RightOrm)
            .where(or_(RightOrm.name == right_old.name, RightOrm.id == right_old.id))
            .values(**right_new.model_dump(exclude_none=True))
            .returning(RightOrm)
        )
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right_old.name or right_old.id}' не существует"))
        except IntegrityError:
            raise ResponseError(ErrorBody(massage=f"Право с названием '{right_new.name}' уже существует"))
        else:
            await self.session.commit()
            return RightModel(id=right_.id, name=right_.name, description=right_.description)

    async def get_all_rights(self) -> RightsModel:
        return RightsModel(
            rights=[
                RightModel(id=right.id, name=right.name, description=right.description)
                for right in (await self.session.scalars(select(RightOrm))).fetchall()
            ]
        )

    async def assign_user_right(self, right: SearchRightModel, user: UserModel) -> ResponseUserModel:
        if not right.model_dump(exclude_none=True) or not user.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt_right = select(RightOrm).where(or_(RightOrm.name == right.name, RightOrm.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))

        stmt_user = (
            select(UserOrm)
            .options(selectinload(UserOrm.rights))
            .where(or_(UserOrm.id == user.id, UserOrm.login == user.login, UserOrm.email == user.email))
        )
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
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt_right = select(RightOrm).where(or_(RightOrm.name == right.name, RightOrm.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(ErrorBody(massage=f"Право '{right.name or right.id}' не существует"))

        stmt_user = (
            select(UserOrm)
            .options(selectinload(UserOrm.rights))
            .where(or_(UserOrm.id == user.id, UserOrm.login == user.login, UserOrm.email == user.email))
        )
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(
                ErrorBody(massage=f"Пользователь '{user.id or user.login or user.email}' не существует")
            )

        try:
            user_.rights.remove(right_)
        except ValueError:
            raise ResponseError(
                ErrorBody(
                    massage=(
                        f"Пользователь '{user.id or user.login or user.email}' "
                        f"не имеет право '{right.name or right.id}'"
                    )
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

    async def get_rights_user(self, user: UserModel) -> RightsModel:
        if not user.model_dump(exclude_none=True):
            raise ResponseError(ErrorBody(massage="Недостаточно информации"))

        stmt = (
            select(UserOrm)
            .options(selectinload(UserOrm.rights))
            .where(or_(UserOrm.id == user.id, UserOrm.login == user.login, UserOrm.email == user.email))
        )
        try:
            rights = (await self.session.scalars(stmt)).unique().one()
        except NoResultFound:
            raise ResponseError(
                ErrorBody(massage=f"Пользователь '{user.id or user.login or user.email}' не существует")
            )

        return RightsModel(
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in rights.rights]
        )


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagement:
    return RightsManagement(redis, postgres)
