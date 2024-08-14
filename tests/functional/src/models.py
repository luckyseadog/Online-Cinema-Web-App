from typing import TypedDict

from pydantic import BaseModel


class GenresTD(TypedDict):
    uuid: str
    name: str


class PersonTD(TypedDict):
    uuid: str
    full_name: str


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None
    description: str | None
    genres: list[GenresTD]
    actors: list[PersonTD]
    writers: list[PersonTD]
    directors: list[PersonTD]


class Genre(BaseModel):
    uuid: str
    name: str
    description: str | None
    films: list[str]


class FilmPersonTD(TypedDict):
    uuid: str
    roles: list[str]


class Person(BaseModel):
    uuid: str
    full_name: str
    films: list[FilmPersonTD]
