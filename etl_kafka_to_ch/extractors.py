import io
from collections.abc import AsyncIterator
from typing import Self

import backoff
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError, KafkaError
from avro.datafile import DataFileReader
from avro.io import DatumReader
from pydantic import ValidationError

from configs.settings import settings
from models import Event


logger = settings.logger


class KafkaExtractor:
    def __init__(self) -> None:
        self.get_consumer()

    def _avro_deserializer(self, data: bytes) -> DataFileReader:
        return DataFileReader(io.BytesIO(data), DatumReader())

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    def get_consumer(self) -> None:
        self.consumer = AIOKafkaConsumer(
            settings.kafka_topic,
            group_id=settings.kafka_group_id,
            bootstrap_servers=settings.kafka_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=self._avro_deserializer,
        )

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aenter__(self) -> Self:
        await self.consumer.start()
        return self

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if exc_type is None:
            await self.consumer.commit()

        await self.consumer.stop()

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def extract(self) -> AsyncIterator[Event | None]:
        try:
            data = await self.consumer.getmany(timeout_ms=100)
        except KafkaError:
            logger.exception("Ошибка при получении сообщений от kafka")
        else:
            if not data:
                logger.info("Нет новых сообщений от kafka")

            for topic_partition, messages in data.items():
                logger.info(f"Получил {len(messages)} сообщений от kafka,  тема {topic_partition.topic}")
                for message in messages:
                    if (values := message.value) is None:
                        continue

                    for value in values:
                        logger.info(f"Сообщение: {value}")
                        try:
                            event = Event.model_validate(value)
                        except ValidationError:
                            logger.exception(f"Ошибка при анализе данных события {data}")
                        else:
                            yield event
