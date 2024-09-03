from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any

import pytest_asyncio
from aiohttp import ClientSession

from core.settings import test_settings


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int]]]:
    async def inner(endpoint: str, query_data: dict[str, str] | None = None) -> tuple[Any, int]:
        url = test_settings.service_url + f"api/v1/{endpoint}"
        async with aio_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status

        return body, status

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]]:
    async def inner(endpoint: str, **kwargs: Any) -> tuple[Any, int]:
        url = test_settings.service_url_auth + f"auth/v1/{endpoint}"
        async with aio_session.post(url, **kwargs) as response:
            body = await response.json()
            status = response.status
            cookies = response.cookies

        return body, status, cookies

    return inner
