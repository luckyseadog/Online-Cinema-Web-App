from base64 import urlsafe_b64encode
from collections.abc import Callable, Coroutine
from hashlib import pbkdf2_hmac
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models_auth import AccountModel, LoginModel
from testdata.alchemy_model import User


APP_ITERS = 100_000
SALT = b"<salt>"


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"name": "login", "password": "password", "login": True},
            {"status": (HTTPStatus.OK, HTTPStatus.UNAUTHORIZED), "length": (2, 1)},
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_refresh(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    pg_session: AsyncSession,
    query_data: dict[str, str],
    expected_answer: dict[str, tuple[int, int]],
) -> None:
    # 1. Создаем таблицы в базе данных

    await create_database()

    # 2. Генерируем данные

    password_enc = query_data["password"].encode("utf-8")
    password_hash_bytes = pbkdf2_hmac("sha256", password_enc, SALT, APP_ITERS)
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

    # 4. Логинимся

    _, _, cookies = await make_post_request(
        "auth/login/", json=login.model_dump(), headers={"user-agent": "test", "sec-ch-ua-platform": "test"}
    )

    # 5. Запрашиваем актуальный токен

    body, status, _ = await make_post_request("auth/refresh/", cookies=cookies)

    # 6. Проверяем ответ

    assert status == expected_answer["status"][0]
    assert len(body) == expected_answer["length"][0]

    # 7. Логаут

    await make_post_request("auth/logout/", cookies=cookies)

    # 8. Запрашиваем актуальный токен после логаута

    body, status, _ = await make_post_request("auth/refresh/", cookies=cookies)

    # 9. Проверяем ответ

    assert status == expected_answer["status"][1]
    assert len(body) == expected_answer["length"][1]

    # 10. Стираем таблицы  в базе данных

    await drop_database()
