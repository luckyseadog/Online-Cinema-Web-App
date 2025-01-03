from uuid import UUID

from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    massage: str


class CreateRightModel(BaseModel):
    name: str
    description: str | None = Field(default=None)


class RightModel(BaseModel):
    id: UUID
    name: str
    description: str | None


class SearchRightModel(BaseModel):
    id: UUID | None = Field(default=None)
    name: str | None = Field(default=None)


class ChangeRightModel(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)


class UserModel(BaseModel):
    id: UUID | None = Field(default=None)
    login: str | None = Field(default=None)
    email: str | None = Field(default=None)
