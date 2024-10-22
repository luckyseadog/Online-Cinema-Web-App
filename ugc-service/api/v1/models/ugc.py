from uuid import UUID

from pydantic import BaseModel, Field


class RatingModel(BaseModel):
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
    rating: float = Field(description="Рейтинг фильма", title="Рейтинг")


class ReviewModel(BaseModel):
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
    review: str = Field(description="Обзор фильма пользователем", title="Обзор")


class FavouriteModel(BaseModel):
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
