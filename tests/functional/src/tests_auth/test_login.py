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


APP_ITERS = 100_000
SALT = b"<salt>"


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ({"login": "login", "password": "password", "create": True}, {"status": HTTPStatus.OK, "length": 2}),
        ({"login": "log", "password": "password", "create": False}, {"status": HTTPStatus.UNAUTHORIZED, "length": 1}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_login(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    pg_session: AsyncSession,
    query_data: dict[str, str],
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных

    await create_database()

    # 2. Генерируем данные

    password_enc = query_data["password"].encode("utf-8")
    password_hash_bytes = pbkdf2_hmac("sha256", password_enc, SALT, APP_ITERS)
    password = urlsafe_b64encode(password_hash_bytes).decode("utf-8")

    login = LoginModel(login=query_data["login"], password=query_data["password"])

    account = AccountModel(
        login=query_data["login"],
        password=password,
        first_name="first_name",
        last_name="last_name",
        email="email",
    )

    # 3. Создаем пользователя в бд

    if query_data["create"]:
        pg_session.add(User(**account.model_dump()))
        await pg_session.commit()

    # 4. Логинимся

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_url_auth}auth/v1/auth/login/",
        json=login.model_dump(),
        headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
    )

    # 5. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 6. Стираем таблицы  в базе данных

    await drop_database()
