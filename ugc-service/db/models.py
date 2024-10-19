from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class Rating(Document):
    user_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    film_id: UUID = Field(default_factory=uuid4)
    rating: float

    class Settings:
        name = "ratings"


class Review(Document):
    user_id: UUID = Field(default_factory=uuid4)
    film_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    review: str

    class Settings:
        name = "reviews"


class Favourite(Document):
    user_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    film_id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "favourites"
