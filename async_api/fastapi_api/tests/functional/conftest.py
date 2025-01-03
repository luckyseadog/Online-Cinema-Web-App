import asyncio
import json
import os

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from pydantic import BaseModel
from redis.asyncio import Redis
from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import GENRES, MOVIES, PERSONS


class Response(BaseModel):
    body: list[dict] | dict
    status: int


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}')
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(scope='session')
async def es_write_data(es_client):
    index_settings = [('movies', MOVIES), ('persons', PERSONS), ('genres', GENRES)]

    for index, settings in index_settings:
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        data = json.loads(settings)
        await es_client.indices.create(index=index, body=data)

        path, _ = os.path.split(os.path.realpath(__file__))
        with open(f'{path}/testdata/data/{index}_test_data.json') as f:
            data = json.load(f)

        actions = [
            {
                '_index': index,
                '_id': doc['id'],
                '_source': doc,
            }
            for doc in data
        ]

        _, errors = await async_bulk(client=es_client, actions=actions, refresh=True)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')


@pytest_asyncio.fixture(scope='session')
async def aiohttp_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield redis
    await redis.aclose()


@pytest_asyncio.fixture(name='make_request')
async def make_request(aiohttp_client):
    async def inner(url, query_data=None):

        async with aiohttp_client.get(url=url, params=query_data) as response:
            return Response(
                body=await response.json(),
                status=response.status,
            )
    return inner
