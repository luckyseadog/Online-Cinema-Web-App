from collections.abc import Sequence
from functools import lru_cache
from uuid import UUID

from api.v1.models import PostFavouriteModel, PostRatingModel, PostReviewModel
from api.v1.models.ratings import PatchRatingModel
from api.v1.models.reviews import PatchReviewModel
from db.models import Favourite, Rating, Review


class UGCService:
    async def get_favourites(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Favourite]:
        return await Favourite.find_many(
            Favourite.user_id == user_id if user_id else {}, Favourite.film_id == film_id if film_id else {}
        ).to_list()

    async def add_to_favourites(self, favourite: PostFavouriteModel) -> Favourite | None:
        if favourite_found := await Favourite.find_one(
            Favourite.user_id == favourite.user_id, Favourite.film_id == favourite.film_id
        ):
            return favourite_found
        else:
            return await Favourite.insert_one(Favourite.model_validate(favourite.model_dump()))

    async def remove_from_favourites(self, favourite_id: UUID) -> None:
        await Favourite.find_one(Favourite.id == favourite_id).delete()

    async def get_ratings(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Rating]:
        return await Rating.find_many(
            Rating.user_id == user_id if user_id else {}, Rating.film_id == film_id if film_id else {}
        ).to_list()

    async def add_rating(self, rating: PostRatingModel) -> Rating | None:
        if rating_found := await Rating.find_one(Rating.user_id == rating.user_id, Rating.film_id == rating.film_id):
            rating_found.rating = rating.rating
            await rating_found.save()
            return rating_found
        else:
            return await Rating.insert_one(Rating.model_validate(rating.model_dump()))

    async def update_rating(self, rating_id: UUID, rating: PatchRatingModel) -> Rating:
        rating_found = await Rating.find_one(Rating.id == rating_id)
        if rating_found:
            rating_found.rating = rating.rating
            await rating_found.save()
            return rating_found
        else:
            raise ValueError("Rating not found")

    async def delete_rating(self, rating_id: UUID) -> None:
        await Rating.find_one(Rating.id == rating_id).delete()

    async def get_reviews(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Review]:
        return await Review.find_many(
            Review.user_id == user_id if user_id else {}, Review.film_id == film_id if film_id else {}
        ).to_list()

    async def add_review(self, review: PostReviewModel) -> Review | None:
        if review_found := await Review.find_one(Review.user_id == review.user_id, Review.film_id == review.film_id):
            review_found.review = review.review
            await review_found.save()
            return review_found
        else:
            return await Review.insert_one(Review.model_validate(review.model_dump()))

    async def update_review(self, review_id: UUID, review: PatchReviewModel) -> Review:
        review_found = await Review.find_one(Review.id == review_id)
        if review_found:
            review_found.review = review.review
            await review_found.save()
            return review_found
        else:
            raise ValueError("Review not found")

    async def delete_review(self, review_id: UUID) -> None:
        await Review.find_one(Review.id == review_id).delete()


@lru_cache
def get_ugc_service() -> UGCService:
    return UGCService()
