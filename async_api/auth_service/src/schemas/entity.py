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
