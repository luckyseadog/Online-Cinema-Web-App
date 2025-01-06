from kafka import KafkaProducer
import json
from functools import lru_cache
from ugc_service.core.config import configs


@lru_cache
def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=configs.kafka_boorstrap_server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )
    return producer