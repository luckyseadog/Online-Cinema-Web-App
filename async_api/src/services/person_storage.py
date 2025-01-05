import backoff
import elasticsearch
from elasticsearch import ElasticsearchException, NotFoundError
from models.film import ShortFilm
from models.person import FilmsByPerson, Person, PersonFilmsRoles
from services.abstract_storage import AbstractStorage
from services.elastic_queries import GET_PERSON_FILMS_AND_ROLES, PERSON_SEARCH

INDEX = 'persons'


class PersonStorage(AbstractStorage):

    def __init__(self, storage):
        self.storage = storage

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_all(self, page_size: int = 50, page_number: int = 0) -> list[Person]:
        try:
            doc = await self.storage.search(
                index=INDEX,
                body={
                    'size': page_size,
                    'from': page_number * page_size,
                },
            )
        except elasticsearch.NotFoundError:
            return None
        return [Person(**hit['_source']) for hit in doc['hits']['hits']]

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def get_by_id(
        self, person_id: str,
        page_size: int = 50,
        page_number: int = 0,
    ) -> PersonFilmsRoles:
        try:
            doc_person = await self.storage.get(index=INDEX, id=person_id)
            doc_films = await self.storage.search(
                index='movies',
                body=GET_PERSON_FILMS_AND_ROLES % (page_number * page_size, page_size, person_id, person_id, person_id),
            )
        except NotFoundError:
            return None
        films = []

        for hit in doc_films['hits']['hits']:
            film = hit['_source']
            roles = []

            for item in film['actors']:
                if item['id'] == person_id:
                    roles.append('actor')
                    break
            for item in film['writers']:
                if item['id'] == person_id:
                    roles.append('writer')
                    break
            for item in film['directors']:
                if item['id'] == person_id:
                    roles.append('director')
                    break

            fp = FilmsByPerson(id=film['id'], roles=roles)
            films.append(fp)
        return PersonFilmsRoles(films=films, **doc_person['_source'])

    @backoff.on_exception(
        backoff.expo,
        (ElasticsearchException,),
        max_tries=3,
        jitter=backoff.random_jitter,
    )
    async def search(self, key: str, page_size: int = 50, page_number: int = 0) -> list[Person]:
        query = PERSON_SEARCH % key
        try:
            doc = await self.storage.search(
                index=INDEX,
                body=query,
            )
        except NotFoundError:
            return None
        return [Person(**hit['_source']) for hit in doc['hits']['hits']]

    async def get_person_films(self, person_id: str, page_size: int = 50, page_number: int = 0) -> list[ShortFilm]:
        doc_movies = await self.storage.search(
            index='movies',
            body=GET_PERSON_FILMS_AND_ROLES % (page_number * page_size, page_size, person_id, person_id, person_id),
        )
        return [ShortFilm(**hit['_source']) for hit in doc_movies['hits']['hits']]
