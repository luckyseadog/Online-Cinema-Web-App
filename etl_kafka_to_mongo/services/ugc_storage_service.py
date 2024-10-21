from functools import lru_cache
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from db.postgres_db import get_session_admin, get_session_ugc
from models.alchemy_model import Favourite, FilmWork, Rating, Review


def update_rating(old_rating: float, new_rating: float) -> float:
    return old_rating * 0.999 + new_rating * 0.001


class UGCStorageService:
    def __init__(self, session: Session, session_admin: Session) -> None:
        self.session = session
        self.session_admin = session_admin

    def _add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> None:
        stmt = select(Rating).where(Rating.user_id == user_id, Rating.film_id == film_id)
        try:
            rating_model = (self.session.scalars(stmt)).one()
            rating_model.rating = rating
            self.session.commit()
        except NoResultFound:
            rating_model = Rating(user_id=user_id, rating=rating, film_id=film_id)
            self.session.add(rating_model)
            self.session.commit()

    def _update_film_rating(self, film_id: UUID, rating: float) -> None:
        stmt = select(FilmWork).where(FilmWork.id == film_id)
        filmwork = self.session_admin.scalars(stmt).one()
        filmwork.rating = update_rating(filmwork.rating, rating)
        self.session_admin.commit()

    def add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> None:
        self._add_rating(user_id, film_id, rating)
        self._update_film_rating(film_id, rating)

    def add_review(self, user_id: UUID, film_id: UUID, review: str) -> None:
        stmt = select(Review).where(Review.user_id == user_id)
        try:
            review_model = (self.session.scalars(stmt)).one()
            review_model.review = review
            self.session.commit()
        except NoResultFound:
            review_ = Review(user_id=user_id, review=review, film_id=film_id)
            self.session.add(review_)
            self.session.commit()

    def add_favourite(self, user_id: UUID, film_id: UUID) -> None:
        stmt = select(Favourite).where(Favourite.user_id == user_id)
        try:
            (self.session.scalars(stmt)).one()
        except NoResultFound:
            favourite_ = Favourite(user_id=user_id, film_id=film_id)
            self.session.add(favourite_)
            self.session.commit()


@lru_cache
def get_ugc_storage_service() -> UGCStorageService:
    session = next(get_session_ugc())
    session_admin = next(get_session_admin())
    return UGCStorageService(session, session_admin)
