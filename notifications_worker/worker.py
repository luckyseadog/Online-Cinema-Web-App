import asyncio
import json
import logging
import logging.config

from kafka import KafkaConsumer
from src.core.config import settings
from src.models.entity import (
    NewMoviesNotification,
    SaleNotification,
    WelcomeNotification,
)
from src.services.notification_service import get_notification_service


class UnprocessableEvent(Exception):
    pass


async def main():
    notification_service = get_notification_service()

    consumer = KafkaConsumer(
        *settings.kafka_topics.split(","),
        bootstrap_servers=[settings.kafka_boorstrap_server],
        auto_offset_reset=settings.kafka_auto_offset_reset,
        enable_auto_commit=False,
        group_id=settings.kafka_group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    while True:
        try:
            for record in consumer:
                message = record.value
                if message["event"] == "welcome-topic":
                    params_batch = [
                        WelcomeNotification(email=email, subject="Greetings") for email in message["emails"]
                    ]
                    await notification_service.send_welcome_many("welcome.txt", params_batch)
                    consumer.commit()
                elif message["event"] == "new-movies-topic":
                    params_batch = [
                        NewMoviesNotification(email=email, movies=message["movies"], subject="You Must Watch This") for email in message["emails"]
                    ]
                    await notification_service.send_new_movies_many("new_movies.txt", params_batch)
                    consumer.commit()
                elif message["event"] == "sale-topic":
                    params_batch = [
                        SaleNotification(email=email, subject="Black Friday Savings Inside!") for email in message["emails"]
                    ]
                    await notification_service.send_sale_many("sale.txt", params_batch)
                    consumer.commit()
                else:
                    event = message["event"]
                    logging.warning(f"No such event: {event}")
                
        except Exception as e:
            logging.warning(f"Error with message: {message}")


if __name__ == "__main__":
    asyncio.run(main())
