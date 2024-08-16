from collections.abc import AsyncGenerator, Iterable, Callable, Coroutine
from typing import Any

import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from core.settings import test_settings


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client() -> AsyncGenerator[AsyncElasticsearch, Any]:
    es_client = AsyncElasticsearch(hosts=test_settings.elastic_dsn, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="es_write_data")
def es_write_data(es_client: AsyncElasticsearch) -> Callable[..., Coroutine[Any, Any, None]]:
    async def inner(data: list[dict[Any, Any]], index: str, mapping: dict[str, Any]) -> None:
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        await es_client.indices.create(index=index, **mapping)

        _, errors = await async_bulk(client=es_client, actions=data, refresh="wait_for")

        if errors:
            raise Exception(f"Ошибки записи данных в Elasticsearch:\n{errors}")

    return inner


@pytest_asyncio.fixture(name="es_clear_data")
def es_clear_data(es_client: AsyncElasticsearch) -> Callable[..., Coroutine[Any, Any, None]]:
    async def inner(indexs: Iterable[str]) -> None:
        for index in indexs:
            await es_client.indices.delete(index=index)

    return inner
