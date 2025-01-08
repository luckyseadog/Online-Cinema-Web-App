import json
import logging
from functools import lru_cache
from typing import Any

from kafka import KafkaProducer
from src.core.config import settings


def on_send_success(record_metadata):
    logging.debug(f"success: {record_metadata}")


def on_send_error(excp):
    raise excp


class NotificationService:
    WELCOME_TOPIC = "welcome-topic"
    NEW_MOVIES_TOPIC = "new-movies-topic"
    SALE_TOPIC = "sale-topic"

    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=[settings.kafka_boorstrap_server],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )

    def _send_notification(self, topic: str, data: dict[Any]):
        self.kafka_producer.send(topic, data).add_callback(on_send_success).add_errback(on_send_error)

    def send_welcome_event(self, template_name: str, emails: list[str], **kwargs):
        data = {"event": self.WELCOME_TOPIC, "template_name": template_name, "emails": emails, **kwargs}
        self._send_notification(self.WELCOME_TOPIC, data)

    def send_new_movies_event(self, template_name: str, emails: list[str], movies: list[Any], **kwargs):
        data = {
            "event": self.NEW_MOVIES_TOPIC,
            "template_name": template_name,
            "emails": emails,
            "movies": movies,
            **kwargs,
        }
        self._send_notification(self.NEW_MOVIES_TOPIC, data)

    def send_sale_event(self, template_name: str, emails: list[str], **kwargs):
        data = {"event": self.SALE_TOPIC, "template_name": template_name, "emails": emails, **kwargs}
        self._send_notification(self.SALE_TOPIC, data)

    def wait_for_send(self):
        self.kafka_producer.flush()


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
