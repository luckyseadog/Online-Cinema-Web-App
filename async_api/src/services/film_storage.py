import backoff
from db.abstruct import StorageInterface
from elasticsearch import ElasticsearchException, NotFoundError
from models.film import Film, SortModel
from models.genre import Genre
from models.person import Person
from services.abstract_storage import AbstractStorage
from services.elastic_queries import (GET_ALL_FILMS, GET_ALL_FILMS_IN_GENRE,
                                      GET_GENRE_BY_NAME, SEARCH_FILMS)

INDEX = 'movies'


class FilmStorage(AbstractStorage):
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_by_id(self, film_id: str) -> Film | None:
        try:
            doc = await self.storage.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        row = doc['_source']
        genre = []
        for el in row['genres']:
            query_genre = GET_GENRE_BY_NAME % (el)
            doc_genre = await self.storage.search(body=query_genre, index='genres')
            genre.append(Genre(**doc_genre['hits']['hits'][0]['_source']))

        directors = [Person(**person) for person in row['directors']]
        actors = [Person(**person) for person in row['actors']]
        writers = [Person(**person) for person in row['writers']]

        return Film(
            id=row['id'],
            title=row['title'],
            imdb_rating=row['imdb_rating'],
            description=row['description'],
            genre=genre,
            directors=directors,
            actors=actors,
            writers=writers,
        )

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_all(
            self,
            page_size: int,
            page_number: int,
            genre: str | None,
            sort: SortModel | None,
    ) -> list[Film]:
        sort_mode = 'asc' if sort == SortModel.ascending else 'desc'
        if genre:
            query = GET_ALL_FILMS_IN_GENRE % (page_size * page_number, page_size, genre, sort_mode)
        else:
            query = GET_ALL_FILMS % (page_size * page_number, page_size, sort_mode)

        doc = await self.storage.search(body=query, index='movies')
        total_size = doc['hits']['total']['value']
        if page_size * page_number >= total_size:
            return None

        data = doc['hits']['hits']
        films = []
        for row_with_meta in data:
            row = row_with_meta['_source']
            films.append(
                Film(
                    id=row['id'],
                    title=row['title'],
                    imdb_rating=row['imdb_rating'],
                ),
            )
        return films

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def search(self, query: str, page_size: int, page_number: int) -> list[Film] | None:
        query = SEARCH_FILMS % (page_size * page_number, page_size, query)
        doc = await self.storage.search(body=query, index='movies')
        total_size = doc['hits']['total']['value']
        if total_size == 0:
            return None

        data = doc['hits']['hits']
        resp = []
        for row_with_meta in data:
            row = row_with_meta['_source']
            resp.append(
                Film(
                    id=row['id'],
                    title=row['title'],
                    imdb_rating=row['imdb_rating'],
                ),
            )
        return resp
