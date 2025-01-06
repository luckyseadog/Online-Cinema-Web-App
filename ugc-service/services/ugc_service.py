from collections.abc import Sequence
from functools import lru_cache
from uuid import UUID

from db.models import Favourite, Rating, Review


class UGCService:
    async def get_favourites(self, user_id: UUID, film_id: UUID | None) -> Sequence[Favourite]:
        return await Favourite.find_many(
            Favourite.user_id == user_id if user_id else {}, Favourite.film_id == film_id if film_id else {}
        ).to_list()

    async def add_to_favourites(self, user_id: UUID, film_id: UUID) -> Favourite | None:
        if favourite_found := await Favourite.find_one(Favourite.user_id == user_id, Favourite.film_id == film_id):
            return favourite_found
        else:
            return await Favourite.insert_one(Favourite(user_id=user_id, film_id=film_id))

    async def remove_from_favourites(self, user_id: UUID, film_id: UUID) -> None:
        await Favourite.find_one(Favourite.user_id == user_id, Favourite.film_id == film_id).delete()

    async def remove_all_favourites(self, user_id: UUID) -> None:
        await Favourite.find_many(Favourite.user_id == user_id).delete()

    async def get_ratings(self, user_id: UUID, film_id: UUID | None) -> Sequence[Rating]:
        return await Rating.find_many(
            Rating.user_id == user_id if user_id else {}, Rating.film_id == film_id if film_id else {}
        ).to_list()

    async def add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> Rating | None:
        if rating_found := await Rating.find_one(Rating.user_id == user_id, Rating.film_id == film_id):
            rating_found.rating = rating
            await rating_found.save()
            return rating_found
        else:
            return await Rating.insert_one(Rating(user_id=user_id, film_id=film_id, rating=rating))

    async def update_rating(self, user_id: UUID, film_id: UUID, rating: float) -> Rating | None:
        rating_found = await Rating.find_one(Rating.user_id == user_id, Rating.film_id == film_id)
        if rating_found:
            rating_found.rating = rating
            await rating_found.save()
            return rating_found
        else:
            return None

    async def delete_rating(self, user_id: UUID, film_id: UUID) -> None:
        await Rating.find_one(Rating.user_id == user_id, Rating.film_id == film_id).delete()

    async def delete_all_ratings(self, user_id: UUID) -> None:
        await Rating.find_many(Rating.user_id == user_id).delete()

    async def get_reviews(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Review]:
        return await Review.find_many(
            Review.user_id == user_id if user_id else {}, Review.film_id == film_id if film_id else {}
        ).to_list()

    async def add_review(self, user_id: UUID, film_id: UUID, review: str) -> Review | None:
        if review_found := await Review.find_one(Review.user_id == user_id, Review.film_id == film_id):
            review_found.review = review
            await review_found.save()
            return review_found
        else:
            return await Review.insert_one(Review(user_id=user_id, film_id=film_id, review=review))

    async def update_review(self, user_id: UUID, film_id: UUID, review: str) -> Review | None:
        review_found = await Review.find_one(Review.user_id == user_id, Review.film_id == film_id)
        if review_found:
            review_found.review = review
            await review_found.save()
            return review_found
        else:
            return None

    async def delete_review(self, user_id: UUID, film_id: UUID) -> None:
        await Review.find_one(Review.user_id == user_id, Review.film_id == film_id).delete()

    async def delete_all_reviews(self, user_id: UUID) -> None:
        await Review.find_many(Review.user_id == user_id).delete()


@lru_cache
def get_ugc_service() -> UGCService:
    return UGCService()
