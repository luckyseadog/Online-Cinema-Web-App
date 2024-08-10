from typing import TypedDict

from pydantic import BaseModel


class Genres(TypedDict):
    uuid: str
    name: str


class Person(TypedDict):
    uuid: str
    full_name: str


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None
    description: str | None
    genres: list[Genres]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
