from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class RoleInDB(BaseModel):
    id: UUID
    title: str
    description: str | None = None


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    email: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    roles: list[RoleInDB] | None = []

    class Config:
        orm_mode = True



class RoleCreate(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class UserRoleUUID(BaseModel):
    user_id: UUID
    role_id: UUID


