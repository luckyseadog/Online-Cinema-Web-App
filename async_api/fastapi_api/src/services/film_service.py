from functools import lru_cache
from uuid import UUID
from db.elastic import get_elastic
from db.redis import get_redis
from db.abstruct import CacheInterface, StorageInterface
from fastapi import Depends
from services.cache import Cache
from models.film import Film, SortModel
from services.film_storage import FilmStorage

INDEX = 'movies'


class FilmService:
    def __init__(self, redis: CacheInterface, elasticsearch: StorageInterface):
        self.storage = FilmStorage(elasticsearch)
        self.cache = Cache(redis)

    async def get_by_id(self, film_id: UUID) -> Film | None:
        CACHE_ID = '_'.join([INDEX, 'get_by_id', film_id])
        film = await self.cache.get_one(CACHE_ID, Film)
        if not film:
            film = await self.storage.get_by_id(str(film_id))
            if not film:
                return None
            await self.cache.put_one(CACHE_ID, film)

        return film

    async def get_all(
            self,
            page_size: int,
            page_number: int,
            genre: str | None,
            sort: SortModel | None,
    ) -> list[Film]:
        CACHE_ID = '_'.join([INDEX, 'get_all_films', str(page_size), str(page_number), str(genre), str(sort)])
        films = await self.cache.get_many(Film, CACHE_ID)
        if not films:
            films = await self.storage.get_all(page_size, page_number, genre, sort)
            if not films:
                return None
            await self.cache.put_many(CACHE_ID, films)

        return films

    async def search(self, query: str, page_size: int, page_number: int) -> list[Film] | None:
        CACHE_ID = '_'.join([INDEX, 'film_search', str(query), str(page_size), str(page_number)])
        films = await self.cache.get_many(Film, CACHE_ID)
        if not films:
            films = await self.storage.search(query, page_size, page_number)
            if not films:
                return None
            await self.cache.put_many(CACHE_ID, films)

        return films


@lru_cache
def get_film_service(
        redis: CacheInterface = Depends(get_redis),
        elasticsearch: StorageInterface = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis=redis, elasticsearch=elasticsearch)
