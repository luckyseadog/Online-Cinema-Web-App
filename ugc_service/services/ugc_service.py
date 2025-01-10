from collections.abc import Sequence
from functools import lru_cache
from uuid import UUID
from db.kafka_db import get_producer
from core.config import configs
import logging

from db.models import Favourite, Rating, Review


class UGCService:
    def __init__(self):
        self.kafka_producer = get_producer()

    async def get_favourites(self, user_id: UUID, film_id: UUID | None) -> Sequence[Favourite]:
        return await Favourite.find_many(
            Favourite.user_id == user_id if user_id else {}, Favourite.film_id == film_id if film_id else {}
        ).to_list()

    async def add_to_favourites(self, user_id: UUID, film_id: UUID) -> Favourite | None:
        try:
            self.kafka_producer.send(
                configs.kafka_topic, 
                [
                    {
                    'action': 'favourite',
                    'user_id': str(user_id),
                    'film_id': str(film_id),
                    },
                ]
                
            )
        except Exception as e:
            logging.error(f"Error sending Kafka message: {e}")

    async def remove_from_favourites(self, user_id: UUID, film_id: UUID) -> Favourite | None:
        try:
            self.kafka_producer.send(
                configs.kafka_topic, 
                [
                    {
                        'action': 'unfavourite',
                        'user_id': str(user_id),
                        'film_id': str(film_id),
                    },
                ]
            )
        except Exception as e:
            logging.error(f"Error sending Kafka message: {e}")

    async def get_ratings(self, user_id: UUID, film_id: UUID | None) -> Sequence[Rating]:
        return await Rating.find_many(
            Rating.user_id == user_id if user_id else {}, Rating.film_id == film_id if film_id else {}
        ).to_list()

    async def add_rating(self, user_id: UUID, film_id: UUID, rating: float) -> Rating | None:
        try:
            self.kafka_producer.send(
                configs.kafka_topic, 
                [
                    {
                        'action': 'rate',
                        'user_id': str(user_id),
                        'film_id': str(film_id),
                        'rating': rating,
                    },
                ]
            )
        except Exception as e:
            logging.error(f"Error sending Kafka message: {e}")

    async def get_reviews(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Review]:
        return await Review.find_many(
            Review.user_id == user_id if user_id else {}, Review.film_id == film_id if film_id else {}
        ).to_list()

    async def add_review(self, user_id: UUID, film_id: UUID, review: str) -> Review | None:
        try:
            self.kafka_producer.send(
                configs.kafka_topic, 
                [
                    {
                        'action': 'review',
                        'user_id': str(user_id),
                        'film_id': str(film_id),
                        'review': review,
                    },
                ]
            )
        except Exception as e:
            logging.error(f"Error sending Kafka message: {e}")


@lru_cache
def get_ugc_service() -> UGCService:
    return UGCService()
