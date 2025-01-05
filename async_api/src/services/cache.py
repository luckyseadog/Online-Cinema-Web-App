import logging

from models.film import Film
from models.genre import Genre
from models.person import Person
from services.abstract_cache import AbstractCache

DELIMETER = '<delimiter>'
CACHE_EXPIRE_IN_SECONDS = 60 * 5


class Cache(AbstractCache):
    def __init__(self, redis):
        self.cache = redis

    async def get_one(self, cache_id: str, entity: Person | Genre | Film):
        logging.info('MAKE: get_one_from_cache')
        data = await self.cache.get(cache_id)
        if not data:
            return None
        res = entity.parse_raw(data)
        return res

    async def put_one(self, cache_id: str, entity: Person | Genre | Film) -> None:
        await self.cache.set(cache_id, entity.json(), CACHE_EXPIRE_IN_SECONDS)

    async def get_many(self, model, cache_id: str) -> list[Film | Person | Genre]:
        logging.info('MAKE: get_many_from_cache')
        data = await self.cache.get(cache_id)
        if not data:
            return None
        tmp = data[1:-1].split(bytes(DELIMETER.encode('utf-8')))
        items = []
        for item in tmp:
            items.append(model.parse_raw(item))
        return items

    async def put_many(self, cache_id: str, items: list[Film | Person | Genre]) -> None:
        items_json = '[' + DELIMETER.join([item.json() for item in items]) + ']'
        await self.cache.set(cache_id, items_json, CACHE_EXPIRE_IN_SECONDS)
