from pydantic import BaseModel
from pydantic.fields import Field


class RightModel(BaseModel):
    name: str = Field(description="Название права", title="Название")
    description: str = Field(description="Описание права", title="Описание")
