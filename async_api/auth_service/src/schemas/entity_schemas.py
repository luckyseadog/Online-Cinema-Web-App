from uuid import UUID

from pydantic import BaseModel


class RolePatch(BaseModel):
    title: str | None = None
    description: str | None = None

class UserPatch(BaseModel):
    login: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserCreate(BaseModel):
    login: str
    email: str
    first_name: str
    last_name: str
    password: str

class UserCredentials(BaseModel):
    login: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class AccessTokenData(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int
    roles: list[str]

class RefreshTokenData(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int


class UpdateUserRole(BaseModel):
    role_id: UUID
    user_id: UUID

