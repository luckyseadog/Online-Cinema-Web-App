from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field


class CreateRightModel(BaseModel):
    name: str = Field(description="Название права", title="Название")
    description: str | None = Field(default=None, description="Описание права", title="Описание")


class DeleteRightModel(BaseModel):
    id: UUID | None = Field(default=None, description="Идентификатор права", title="Идентификатор")
    name: str | None = Field(default=None, description="Название права", title="Название")


class ChangeRightModel(BaseModel):
    id: UUID | None = Field(default=None, description="Идентификатор права", title="Идентификатор")
    current_name: str | None = Field(default=None, description="Текущее название права", title="Название")
    name: str | None = Field(default=None, description="Новое название права", title="Новое название")
    description: str | None = Field(default=None, description="Новое описание права", title="Новое описание")


class RightModel(BaseModel):
    id: UUID = Field(description="Идентификатор права", title="Идентификатор")
    name: str = Field(description="Название права", title="Название")
    description: str | None = Field(description="Описание права", title="Описание")


class RightsModel(BaseModel):
    rights: list[RightModel] = Field(description="Список прав", title="Список прав")
