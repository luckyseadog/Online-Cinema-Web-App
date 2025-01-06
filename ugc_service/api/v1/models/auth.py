from uuid import UUID

from fastapi import Request
from pydantic import BaseModel
from pydantic.fields import Field


class JWTUserModel(BaseModel):
    id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    rights: set[str] = Field(description="Права юзера", title="Права")


class JWTRequestModel(Request):
    jwt_user: JWTUserModel = Field(description="Пользователь с аутентификацией", title="Пользователь")
