from typing import TypedDict

from pydantic import BaseModel


class FilmGenre(TypedDict):
    uuid: str
    name: str


class FilmPerson(TypedDict):
    uuid: str
    full_name: str


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None
    description: str | None
    genres: list[FilmGenre]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]


class Genre(BaseModel):
    uuid: str
    name: str
    description: str | None
    films: list[str]


class PersonFilm(TypedDict):
    uuid: str
    roles: list[str]


class Person(BaseModel):
    uuid: str
    full_name: str
    films: list[PersonFilm]
