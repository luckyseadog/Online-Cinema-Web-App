from uuid import UUID

from pydantic import BaseModel, Field


class FavouriteModel(BaseModel):
    id: UUID = Field(description="Идентификатор избранного", title="Идентификатор")
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
