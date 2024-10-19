from collections.abc import Sequence
from functools import lru_cache
from uuid import UUID

from db.models import Favourite, Rating, Review


class UGCService:
    async def get_ratings(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Rating]:
        return await Rating.find_many(
            Rating.user_id == user_id.__str__() if user_id else {},
            Rating.film_id == film_id.__str__() if film_id else {}
        ).to_list()

    async def get_reviews(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Review]:
        return await Review.find_many(
            Review.user_id == user_id.__str__() if user_id else {},
            Review.film_id == film_id.__str__() if film_id else {}
        ).to_list()

    async def get_favourites(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Favourite]:
        return await Favourite.find_many(
            Favourite.user_id == user_id.__str__() if user_id else {},
            Favourite.film_id == film_id.__str__() if film_id else {}
        ).to_list()


@lru_cache
def get_ugc_service() -> UGCService:
    return UGCService()
