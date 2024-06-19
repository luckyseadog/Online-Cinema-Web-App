import datetime
import uuid
from uuid import UUID
from pydantic import BaseModel, Field


class Role(BaseModel):
    # id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    id: UUID
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    login: str
    password: str
    first_name: str
    last_name: str = Field(default_factory=str)
    email: str = Field(default_factory=str)
    is_superadmin: bool = Field(default=False)
    roles: list[Role] | None = None
    deleted_at: datetime.datetime | None = None

    class Config:
        orm_mode = True

class History(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    occured_at: datetime.datetime | None = None
    action: str
    fingerprint: str | None = None


class UserCreate(BaseModel):
    login: str
    email: str
    first_name: str
    last_name: str
    password: str

class UserCredentials(BaseModel):
    login: str
    password: str


class UserRoleUUID(BaseModel):
    user_id: str
    role_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class AccessTokenData(BaseModel):
    iss: str
    sub: str
    roles: list[str]


class UpdateUserRole(BaseModel):
    role_id: UUID
    user_id: UUID
