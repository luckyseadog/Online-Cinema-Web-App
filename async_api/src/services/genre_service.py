from functools import lru_cache

from db.abstruct import CacheInterface, StorageInterface
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.genre import Genre
from services.cache import Cache
from services.genre_storage import GenreStorage

INDEX = 'genres'


class GenreService:
    def __init__(self, redis: CacheInterface, elasticsearch: StorageInterface):
        self.storage = GenreStorage(elasticsearch)
        self.cache = Cache(redis)

    async def get_all(
        self,
        page_size: int = 50,
        page_number: int = 0,
    ) -> list[Genre]:
        CACHE_ID = '_'.join([INDEX, 'get_all', str(page_size), str(page_number)])
        genres = await self.cache.get_many(Genre, CACHE_ID)
        if not genres:
            genres = await self.storage.get_all(page_size, page_number)
            if not genres:
                return None
            await self.cache.put_many(CACHE_ID, genres)
        return genres

    async def get_by_id(self, genre_id: str) -> Genre | None:
        CACHE_ID = '_'.join([INDEX, 'get_by_id', genre_id])
        genre = await self.cache.get_one(CACHE_ID, Genre)
        if not genre:
            genre = await self.storage.get_by_id(genre_id)
            if not genre:
                return None
            await self.cache.put_one(CACHE_ID, genre)
        return genre

    async def search(self, key: str, page_size: int = 50, page_number: int = 0) -> list[Genre]:
        return await self.search(key, page_size, page_number)


@lru_cache
def get_genre_service(
        redis: CacheInterface = Depends(get_redis),
        elasticsearch: StorageInterface = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis=redis, elasticsearch=elasticsearch)
