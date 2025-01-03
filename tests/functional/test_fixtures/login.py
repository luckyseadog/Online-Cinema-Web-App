from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any
from uuid import uuid4

import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_auth import LoginModel
from test_fixtures.password import Password
from testdata.alchemy_model import Right, User


@pytest_asyncio.fixture(name="login_auth")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def login_auth(
    create_database: Callable[[], Coroutine[Any, Any, None]],
    drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    pg_session: AsyncSession,
    compute_hash: Callable[..., Coroutine[Any, Any, Password]],
) -> Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]]:
    async def inner() -> tuple[SimpleCookie, dict[str, str]]:
        await create_database()

        login = "login"
        password = "password"

        right = Right(name="subscriber")
        pg_session.add(right)
        pg_session.add(
            User(
                id=uuid4(),
                login=login,
                password=await compute_hash(password),
                first_name="first_name_assign",
                last_name="last_name_assign",
                email="email_assign",
                rights=[right],
            )
        )
        await pg_session.commit()

        _, _, cookies = await make_post_request(
            url=f"{test_settings.service_url_auth}auth/v1/auth/login/",
            json=LoginModel(login=login, password=password).model_dump(),
        )

        await drop_database()

        headers = {
            "cookie": (
                f"access_token_cookie={cookies.get("access_token_cookie").value}; "
                f"refresh_token_cookie={cookies.get("refresh_token_cookie").value}"
            )
        }
        return cookies, headers

    return inner
