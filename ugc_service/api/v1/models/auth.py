from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field


class UserModel(BaseModel):
    id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
