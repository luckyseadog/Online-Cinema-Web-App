import http
import uuid
from collections.abc import Callable, Coroutine
from typing import Any

import pytest

from core.settings import test_settings
from src.models import Film


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({"query": "The Star"}, {"status": http.HTTPStatus.OK, "length": 10}),
        (
            {"query": "The Star", "sort": "imdb_rating", "page_number": 1, "page_size": 5},
            {"status": http.HTTPStatus.OK, "length": 5},
        ),
        ({"query": "Mashed potato"}, {"status": http.HTTPStatus.BAD_REQUEST, "length": 1}),
        ({"sort": "qwerty"}, {"status": http.HTTPStatus.BAD_REQUEST, "length": 1}),
        ({"page_number": 0}, {"status": http.HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1}),
        ({"page_size": 0}, {"status": http.HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_search(
    es_write_data: Callable[..., Coroutine[Any, Any, None]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    es_clear_data: Callable[..., Coroutine[Any, Any, None]],
    query_data: dict[str, str],
    expected_answer: dict[str, int],
) -> None:
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
        data: dict[str, Any] = {"_index": test_settings.es_index_movies, "_id": row[test_settings.es_id_field]}
        data.update({"_source": row})
        bulk_query.append(data)

    # 2. Загружаем данные в ES

    await es_write_data(bulk_query, test_settings.es_index_movies, test_settings.es_index_mapping_movies)

    # 3. Запрашиваем данные из ES по API

    body, status = await make_get_request("films/search/", query_data)

    # 4. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 5. Очищаем данные в ES

    await es_clear_data((test_settings.es_index_movies,))

    # 6. Запрашиваем данные из Redis по API

    body, status = await make_get_request("films/search/", query_data)

    # 7. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
