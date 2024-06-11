from uuid import UUID

from pydantic import BaseModel, Field
import uuid


class Role(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    login: str
    password: str
    first_name: str
    last_name: str
    email: str
    first_name: str
    last_name: str
    roles: list[Role] = Field(default_factory=[])

    class Config:
        orm_mode = True







