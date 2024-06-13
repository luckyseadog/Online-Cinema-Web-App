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
    last_name: str = Field(default_factory=str)
    email: str = Field(default_factory=str)
    roles: list[Role] | None = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    login: str
    email: str
    first_name: str
    last_name: str
    password: str


class UserRoleUUID(BaseModel):
    user_id: UUID
    role_id: UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None

class UserLogin(BaseModel):
    username: str
    password: str
