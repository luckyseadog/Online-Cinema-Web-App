import http
import uuid
from collections.abc import Callable, Coroutine
from typing import Any

import pytest

from core.settings import test_settings
from src.models_api import Person


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({}, {"status": http.HTTPStatus.OK, "length": 10}),
        ({"page_number": 2, "page_size": 5}, {"status": http.HTTPStatus.OK, "length": 5}),
        ({"page_number": 0}, {"status": http.HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1}),
        ({"page_size": 0}, {"status": http.HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_persons_list(
    es_write_data: Callable[..., Coroutine[Any, Any, None]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    es_clear_data: Callable[..., Coroutine[Any, Any, None]],
    query_data: dict[str, str],
    expected_answer: dict[str, int],
) -> None:
    # 1. Генерируем данные для ES

    es_data = [
        Person(
            uuid=str(uuid.uuid4()),
            full_name="Boris Borisovich",
            films=[
                {"uuid": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "roles": ["writer"]},
                {"uuid": "b45bd7bc-2e16-46d5-b125-983d356768c6", "roles": ["actor"]},
            ],
        ).model_dump()
        for _ in range(60)
    ]
    bulk_query: list[dict[str, Any]] = []
    for row in es_data:
        data: dict[str, Any] = {"_index": test_settings.es_index_persons, "_id": row[test_settings.es_id_field]}
        data.update({"_source": row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES

    await es_write_data(bulk_query, test_settings.es_index_persons, test_settings.es_index_mapping_persons)

    # 3. Запрашиваем данные из ES по API

    body, status = await make_get_request(url=f"{test_settings.service_url}api/v1/persons/", params=query_data)

    # 4. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 5. Очищаем данные в ES

    await es_clear_data((test_settings.es_index_persons,))

    # 6. Запрашиваем данные из Redis по API

    body, status = await make_get_request(url=f"{test_settings.service_url}api/v1/persons/", params=query_data)

    # 7. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
