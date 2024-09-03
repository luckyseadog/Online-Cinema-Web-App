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
        ({"name": "login", "password": "password"}, {"status": HTTPStatus.OK, "length": 4}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_update(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    make_patch_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    pg_session: AsyncSession,
    query_data: dict[str, str],
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

    password_enc = b"password_update"
    password_hash_bytes = pbkdf2_hmac("sha256", password_enc, test_settings.salt_password, test_settings.iters_password)
    password_update = urlsafe_b64encode(password_hash_bytes).decode("utf-8")

    account_update = AccountModel(
        login=f"{query_data["name"]}_update",
        password=password_update,
        first_name="first_name_update",
        last_name="last_name_update",
        email="email_update",
    )
    # 3. Создаем пользователя в бд

    pg_session.add(User(**account.model_dump()))
    await pg_session.commit()

    # 4. Логинимся

    _, _, cookies = await make_post_request(
        url=f"{test_settings.service_url_auth}auth/v1/auth/login/",
        json=login.model_dump(),
        headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
    )

    # 5. Обновляем данные

    body, status, _ = await make_patch_request(
        url=f"{test_settings.service_url_auth}auth/v1/auth/update/", json=account_update.model_dump(), cookies=cookies
    )

    # 6. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 7. Стираем таблицы  в базе данных

    await drop_database()
