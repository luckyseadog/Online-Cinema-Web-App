import logging
import logging.config
from enum import Enum
from io import BytesIO
from typing import NoReturn
from uuid import UUID

import sentry_sdk
from avro.datafile import DataFileReader
from avro.io import DatumReader
from kafka import KafkaConsumer

from core.config import configs
from services.ugc_storage_service import get_ugc_storage_service


class InvalidActionError(Exception):
    pass


class Action(Enum):
    REVIEW_FILM = "review"
    RATE_FILM = "rate"
    FAVOURITE_FILM = "favourite"
    UNFAVOURITE_FILM = "unfavourite"


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


def avro_deserializer(data: bytes) -> DataFileReader:
    return DataFileReader(BytesIO(data), DatumReader())


def main() -> NoReturn:
    ugc_storage_service = get_ugc_storage_service()

    consumer = KafkaConsumer(
        configs.kafka_topic,
        group_id=configs.kafka_group_id,
        bootstrap_servers=configs.kafka_boorstrap_server,
        auto_offset_reset=configs.kafka_auto_offset_reset,
        value_deserializer=avro_deserializer,
    )
    while True:
        try:
            for message in consumer:
                values = message.value

                for value in values:
                    logging.info(f"MASSAGE: {value}")
                    action = value["action"]
                    user_id = UUID(value["user_id"])
                    film_id = UUID(value["film_id"])
                    match action:
                        case Action.REVIEW_FILM.value:
                            ugc_storage_service.add_review(user_id, film_id, value["review"])
                        case Action.RATE_FILM.value:
                            ugc_storage_service.add_rating(user_id, film_id, value["rating"])
                        case Action.FAVOURITE_FILM.value:
                            ugc_storage_service.add_favourite(user_id, film_id)
                        case Action.UNFAVOURITE_FILM.value:
                            ugc_storage_service.del_favourite(user_id, film_id)
                        case _:
                            raise InvalidActionError(f"No such action: {action}")

        except InvalidActionError as e:
            logging.warning(f"Could not process action: {e}")
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Unexpected error occur: {e}")


if __name__ == "__main__":
    main()
