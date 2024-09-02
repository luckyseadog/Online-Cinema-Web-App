from collections.abc import Callable, Coroutine
from typing import Any

import pytest

from testdata.alchemy_model import User


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ("ef86b8ff-3c82-4d31-ad8e-72b69f4e3f9w", "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f9w"),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_creation_of_right(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    # es_write_data: Callable[..., Coroutine[Any, Any, None]],
    # make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    # es_clear_data: Callable[..., Coroutine[Any, Any, None]],
    query_data: dict[str, str],
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных

    await create_database()
    
    # 2. Генерируем данные для БД

    user = User(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        login="login",
        password="",
        first_name="first_name",
        last_name="last_name",
        email="first_name@gmail.com",
    )

    # 3. Идем в auth api

    # 4. Стираем таблицы  в базе данных

    await drop_database()

    # 5. Проверяем ответ

    assert query_data == expected_answer
