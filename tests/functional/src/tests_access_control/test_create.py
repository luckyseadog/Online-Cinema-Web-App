from base64 import urlsafe_b64encode
from collections.abc import Callable, Coroutine
from hashlib import pbkdf2_hmac
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_access_control import CreateRightModel
from src.models_auth import AccountModel, LoginModel
from testdata.alchemy_model import Right, User


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"name": "admin", "right": "admin", "create_right_api": "qwerty", "password": "password"},
            {"status": (HTTPStatus.OK, HTTPStatus.MISDIRECTED_REQUEST), "length": (3, 1)},
        ),
        (
            {"name": "qwerty", "right": "qwerty", "create_right_api": "qwerty", "password": "password"},
            {"status": (HTTPStatus.FORBIDDEN, HTTPStatus.FORBIDDEN), "length": (1, 1)},
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_create(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    pg_session: AsyncSession,
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    query_data: dict[str, str],
    expected_answer: dict[str, tuple[int, int]],
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
    right = Right(name=query_data["right"])

    create_right_api = CreateRightModel(name=query_data["create_right_api"])

    # 3. Создаем пользователя в бд

    if query_data["right"] != "admin":
        pg_session.add(Right(name="admin"))

    pg_session.add(right)
    pg_session.add(User(**account.model_dump(), rights=[right]))
    await pg_session.commit()

    # 4. Логинимся

    _, _, cookies = await make_post_request(
        url=f"{test_settings.service_url_auth}auth/v1/auth/login/",
        json=login.model_dump(),
        headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
    )

    # 5. Создаем право через api

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_url_auth}auth/v1/access_control/rights/create/",
        json=create_right_api.model_dump(),
        cookies=cookies,
    )

    # 6. Проверяем ответ

    assert status == expected_answer["status"][0]
    assert len(body) == expected_answer["length"][0]

    # 7. Повторно создаем право через api

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_url_auth}auth/v1/access_control/rights/create/",
        json=create_right_api.model_dump(),
        cookies=cookies,
    )

    # 8. Проверяем ответ

    assert status == expected_answer["status"][1]
    assert len(body) == expected_answer["length"][1]

    # 9. Стираем таблицы  в базе данных

    await drop_database()
