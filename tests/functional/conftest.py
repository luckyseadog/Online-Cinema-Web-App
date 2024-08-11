import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from core.settings import test_settings

@pytest_asyncio.fixture(name="es_client")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.elastic_dsn, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="es_write_data")
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(bulk_query: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)

        _, errors = await async_bulk(client=es_client, actions=bulk_query, refresh="wait_for")

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner
