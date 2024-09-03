import http
from collections.abc import Callable, Coroutine
from typing import Any

import pytest
from aiohttp import ClientSession

from core.settings import test_settings
from src.models_auth import AccountModel


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({"login": "Petr"}, {"status": (http.HTTPStatus.OK, http.HTTPStatus.CONFLICT), "length": (4, 1)}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_register(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    query_data: dict[str, str],
    expected_answer: dict[str, tuple[int, int]],
) -> None:
    # 1. Создаем таблицы в базе данных

    await create_database()

    # 2. Генерируем данные

    account = AccountModel(
        login=query_data["login"],
        password="password",  # noqa: S106
        first_name="first_name",
        last_name="last_name",
        email="email",
    )

    # 3. Создаем аккаунт в бд через auth api

    url = test_settings.service_url_auth + "auth/v1/auth/register/"
    async with ClientSession() as aio_session, aio_session.post(url, json=account.model_dump()) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ

    assert status == expected_answer["status"][0]
    assert len(body) == expected_answer["length"][0]

    # 5. Пытаемся повторно создать аккаунт в бд через auth api

    url = test_settings.service_url_auth + "auth/v1/auth/register/"
    async with ClientSession() as aio_session, aio_session.post(url, json=account.model_dump()) as response:
        body = await response.json()
        status = response.status

    # 6. Проверяем ответ

    assert status == expected_answer["status"][1]
    assert len(body) == expected_answer["length"][1]

    # 7. Стираем таблицы  в базе данных

    await drop_database()
