import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    email: str

    class ConfigDict:
        from_attributes = True
