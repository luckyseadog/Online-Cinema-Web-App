from uuid import UUID

from pydantic import BaseModel, Field


class RatingModel(BaseModel):
    id: UUID = Field(description="Идентификатор рейтинга", title="Идентификатор")
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
    rating: float = Field(description="Рейтинг фильма", title="Рейтинг")


class PostRatingModel(BaseModel):
    rating: float = Field(description="Рейтинг фильма", title="Рейтинг")


class PatchRatingModel(BaseModel):
    rating: float = Field(description="Рейтинг фильма", title="Рейтинг")
