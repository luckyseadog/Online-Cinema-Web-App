import datetime
import uuid
from uuid import UUID

from pydantic import BaseModel, Field


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

class History(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID
    occured_at: datetime.datetime
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

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


