from models.genre import Genre
from models.mixins import OrjsonMixin, UUIDMixin
from models.person import Person
from enum import Enum


class ShortFilm(UUIDMixin, OrjsonMixin):
    title: str
    imdb_rating: float | None = None

class FullFilm(ShortFilm):
    description: str | None = None
    genre: list[Genre] | None = None
    directors: list[Person] | None = None
    actors: list[Person] | None = None
    writers: list[Person] | None = None

class Film(UUIDMixin, OrjsonMixin):
    title: str
    imdb_rating: float | None = None
    description: str | None = None
    genre: list[Genre] | None = None
    directors: list[Person] | None = None
    actors: list[Person] | None = None
    writers: list[Person] | None = None

class SortModel(str, Enum):
    descending = '-imdb_rating'
    ascending = 'imdb_rating'
