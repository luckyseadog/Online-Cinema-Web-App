from functools import lru_cache

from db.abstruct import CacheInterface, StorageInterface
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.person import Person, PersonFilmsRoles
from services.abstract_service import AbstractService
from services.cache import Cache
from services.person_storage import PersonStorage

INDEX = 'persons'


class PersonService(AbstractService):
    def __init__(self, redis: CacheInterface, elasticsearch: StorageInterface):
        self.storage = PersonStorage(elasticsearch)
        self.cache = Cache(redis)

    async def get_all(self, page_size: int = 50, page_number: int = 0):
        CACHE_ID = '_'.join([INDEX, str(page_size), str(page_number)])
        persons = await self.cache.get_many(Person, CACHE_ID)
        if not persons:
            persons = await self.storage.get_all(page_size, page_number)
            if not persons:
                return None
            await self.cache.put_many(CACHE_ID, persons)
        return persons

    async def get_by_id(self, person_id: str) -> PersonFilmsRoles | None:
        CACHE_ID = '_'.join([INDEX, 'get_by_id', person_id])
        person = await self.cache.get_one(CACHE_ID, PersonFilmsRoles)
        if not person:
            person = await self.storage.get_by_id(person_id)
            if not person:
                return None
            await self.cache.put_one(CACHE_ID, person)
        return person

    async def search(self, key: str, page_size: int = 50, page_number: int = 0) -> list[PersonFilmsRoles]:
        persons = await self.storage.search(key, page_size, page_number)
        return [await self.storage.get_by_id(person.id) for person in persons]

    async def get_person_films(self, person_id, page_size: int = 50, page_number: int = 0):
        return await self.storage.get_person_films(person_id, page_size, page_number)


@lru_cache
def get_person_service(
        redis: CacheInterface = Depends(get_redis),
        elasticsearch: StorageInterface = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis=redis, elasticsearch=elasticsearch)
