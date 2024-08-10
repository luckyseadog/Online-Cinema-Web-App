import uuid
from typing import Any

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from core.settings import test_settings
from src.models import Film

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`,
#               который следит за запуском и работой цикла событий.


@pytest.mark.asyncio
async def test_search() -> None:
    # 1. Генерируем данные для ES

    es_data = [
        Film(
            uuid=str(uuid.uuid4()),
            imdb_rating=8.5,
            title="The Star",
            description="New World",
            genres=[
                {"uuid": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f9q", "name": "Sci-Fi"},
                {"uuid": "fb111f22-121e-44a7-b78f-b19191810fbq", "name": "Action"},
            ],
            actors=[
                {"uuid": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95", "full_name": "Ann"},
                {"uuid": "fb111f22-121e-44a7-b78f-b19191810fbf", "full_name": "Bob"},
            ],
            writers=[
                {"uuid": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "full_name": "Ben"},
                {"uuid": "b45bd7bc-2e16-46d5-b125-983d356768c6", "full_name": "Howard"},
            ],
            directors=[],
        ).model_dump()
        for _ in range(60)
    ]
    bulk_query: list[dict[str, Any]] = []
    for row in es_data:
        data: dict[str, Any] = {"_index": "movies", "_id": row["uuid"]}
        data.update({"_source": row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES

    es_client = AsyncElasticsearch(hosts=test_settings.elastic_dsn, verify_certs=False)
    if await es_client.indices.exists(index=test_settings.es_index):
        await es_client.indices.delete(index=test_settings.es_index)
    await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)

    _, errors = await async_bulk(client=es_client, actions=bulk_query, refresh="wait_for")

    await es_client.close()

    if errors:
        raise Exception("Ошибка записи данных в Elasticsearch")

    # 3. Запрашиваем данные из ES по API

    url = test_settings.service_url + "api/v1/films/search/"
    query_data = {"query": "Star"}
    session = aiohttp.ClientSession()
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
    await session.close()

    # 4. Проверяем ответ

    assert status == 200
    assert len(body) == 10
