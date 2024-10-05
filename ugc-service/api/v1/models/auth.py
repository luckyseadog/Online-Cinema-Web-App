from pydantic import BaseModel
from pydantic.fields import Field


class JWTUserModel(BaseModel):
    id: str = Field(description="Идентификатор юзера", title="Идентификатор")
    rights: set[str] = Field(description="Права юзера", title="Права")
