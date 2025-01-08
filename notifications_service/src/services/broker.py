from typing import Self

from faststream.kafka import KafkaBroker
from faststream.kafka.fastapi import KafkaRouter
from src.core.config import settings


class KafkaService:
    router: KafkaRouter = KafkaRouter(
        settings.kafka_server,
        asyncapi_url='/asyncapi',
    )

    @property
    def broker(self: Self) -> KafkaBroker:
        return self.router.broker
