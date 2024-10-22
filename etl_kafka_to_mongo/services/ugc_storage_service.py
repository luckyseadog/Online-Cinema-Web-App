from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

from pymongo.synchronous.database import Database
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.mongo_db import get_db_ugc
from db.postgres_db import get_session_admin
from models.alchemy_model import FilmWork


def update_rating(old_rating: float, new_rating: float) -> float:
    return old_rating * 0.999 + new_rating * 0.001


class UGCStorageService:
    def __init__(self, mongo_db: Database[Any], session_admin: Session) -> None:
        self.mongo_db = mongo_db
        self.session_admin = session_admin

    def _add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> None:
        if existing_document := self.mongo_db.ratings.find_one({"user_id": user_id, "film_id": film_id}):
            self.mongo_db.ratings.update_one({"_id": existing_document["_id"]}, {"$set": {"rating": rating}})
        else:
            self.mongo_db.ratings.insert_one({"_id": uuid4(), "user_id": user_id, "film_id": film_id, "rating": rating})

    def _update_film_rating(self, film_id: UUID, rating: float) -> None:
        stmt = select(FilmWork).where(FilmWork.id == film_id)
        filmwork = self.session_admin.scalars(stmt).one()
        filmwork.rating = update_rating(filmwork.rating, rating)
        self.session_admin.commit()

    def add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> None:
        self._add_rating(user_id, film_id, rating)
        self._update_film_rating(film_id, rating)

    def add_review(self, user_id: UUID, film_id: UUID, review: str) -> None:
        if existing_document := self.mongo_db.reviews.find_one({"user_id": user_id, "film_id": film_id}):
            self.mongo_db.reviews.update_one({"_id": existing_document["_id"]}, {"$set": {"review": review}})
        else:
            self.mongo_db.reviews.insert_one({"_id": uuid4(), "user_id": user_id, "film_id": film_id, "review": review})

    def add_favourite(self, user_id: UUID, film_id: UUID) -> None:
        if not self.mongo_db.favourites.find_one({"user_id": user_id, "film_id": film_id}):
            self.mongo_db.favourites.insert_one({"_id": uuid4(), "user_id": user_id, "film_id": film_id})

    def del_favourite(self, user_id: UUID, film_id: UUID) -> None:
        if self.mongo_db.favourites.find_one({"user_id": user_id, "film_id": film_id}):
            self.mongo_db.favourites.delete_one({"user_id": user_id, "film_id": film_id})


@lru_cache
def get_ugc_storage_service() -> UGCStorageService:
    session = get_db_ugc()
    session_admin = next(get_session_admin())
    return UGCStorageService(session, session_admin)
