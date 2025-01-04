from services.abstract_storage import AbstractStorage
from db.abstruct import StorageInterface
from elasticsearch import NotFoundError, ElasticsearchException
from models.genre import Genre
import backoff
INDEX = 'genres'


class GenreStorage(AbstractStorage):
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_all(self, page_size: int, page_number: int) -> list[Genre]:
        try:
            doc = await self.storage.search(
                index=INDEX,
                body={
                    'size': page_size,
                    'from': page_number,
                },
            )
        except NotFoundError:
            return None
        return [Genre(**hit['_source']) for hit in doc['hits']['hits']]

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.storage.get(index=INDEX, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def search(self, key: str, page_size: int = 50, page_number: int = 0) -> list[Genre] | None:
        doc = await self.storage.search(
            index=INDEX,
            body={
                'size': page_size,
                'from': page_number,
                'query': {
                    'match': {'name': {'query': key, 'fuzziness': 'auto'}},
                },
            },
        )
        return [Genre(**hit['_source']) for hit in doc['hits']['hits']]
