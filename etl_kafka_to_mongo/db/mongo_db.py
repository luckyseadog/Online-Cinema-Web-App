from functools import lru_cache
from typing import Any

from pymongo import MongoClient
from pymongo.synchronous.database import Database

from core.config import configs


@lru_cache
def get_db_ugc() -> Database[Any]:
    client: MongoClient[Any] = MongoClient(
        configs.mongo_host_ugc, configs.mongo_port_ugc, uuidRepresentation="standard"
    )
    return client[configs.mongo_name]
