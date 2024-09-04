from base64 import urlsafe_b64encode
from collections.abc import Callable, Coroutine
from hashlib import pbkdf2_hmac
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_auth import AccountModel, LoginModel
from testdata.alchemy_model import User


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"name": "login", "password": "password", "iters": 5, "page_number": 1, "page_size": 3},
            {"status": HTTPStatus.OK, "length": 3},
        ),
        (
            {"name": "login", "password": "password", "iters": 5, "page_number": 2, "page_size": 3},
            {"status": HTTPStatus.OK, "length": 2},
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_history(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    pg_session: AsyncSession,
    query_data: dict[str, str | int],
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных

    await create_database()

    # 2. Генерируем данные

    password_enc = query_data["password"].encode("utf-8")
    password_hash_bytes = pbkdf2_hmac("sha256", password_enc, test_settings.salt_password, test_settings.iters_password)
    password = urlsafe_b64encode(password_hash_bytes).decode("utf-8")

    login = LoginModel(login=query_data["name"], password=query_data["password"])

    account = AccountModel(
        login=query_data["name"],
        password=password,
        first_name="first_name",
        last_name="last_name",
        email="email",
    )

    # 3. Создаем пользователя в бд

    pg_session.add(User(**account.model_dump()))
    await pg_session.commit()

    # 4. Логинимся несколько раз

    for _ in range(query_data["iters"]):
        _, _, cookies = await make_post_request(
            url=f"{test_settings.service_url_auth}auth/v1/auth/login/",
            json=login.model_dump(),
            headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
        )

    # 5. Получаем историю login/logout

    body, status = await make_get_request(
        url=f"{test_settings.service_url_auth}auth/v1/auth/history/",
        cookies=cookies,
        params={"page_number": query_data["page_number"], "page_size": query_data["page_size"]},
    )

    # 6. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 7. Стираем таблицы  в базе данных

    await drop_database()
