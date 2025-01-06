from uuid import UUID

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    id: UUID = Field(description="Идентификатор рецензии", title="Идентификатор")
    user_id: UUID = Field(description="Идентификатор юзера", title="Идентификатор")
    film_id: UUID = Field(description="Идентификатор фильма", title="Идентификатор")
    review: str = Field(description="Рецензия фильма пользователем", title="Рецензия")


class PostReviewModel(BaseModel):
    review: str = Field(description="Рецензия фильма пользователем", title="Рецензия")


class PatchReviewModel(BaseModel):
    review: str = Field(description="Рецензия фильма пользователем", title="Рецензия")
