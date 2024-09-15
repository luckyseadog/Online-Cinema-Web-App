from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any

import pytest_asyncio
from aiohttp import ClientSession


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int]]]:
    async def inner(**kwargs: Any) -> tuple[Any, int]:
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"X-Request-Id": "12345"}
        else:
            kwargs["headers"]["X-Request-Id"] = "test_id"

        async with aio_session.get(**kwargs) as response:
            body = await response.json()
            status = response.status

        return body, status

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]]:
    async def inner(**kwargs: Any) -> tuple[Any, int, SimpleCookie]:
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"X-Request-Id": "12345"}
        else:
            kwargs["headers"]["X-Request-Id"] = "test_id"

        async with aio_session.post(**kwargs) as response:
            body = await response.json()
            status = response.status
            cookies = response.cookies

        return body, status, cookies

    return inner


@pytest_asyncio.fixture(name="make_put_request")
def make_put_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]]:
    async def inner(**kwargs: Any) -> tuple[Any, int, SimpleCookie]:
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"X-Request-Id": "12345"}
        else:
            kwargs["headers"]["X-Request-Id"] = "test_id"

        async with aio_session.put(**kwargs) as response:
            body = await response.json()
            status = response.status
            cookies = response.cookies

        return body, status, cookies

    return inner


@pytest_asyncio.fixture(name="make_patch_request")
def make_patch_request(aio_session: ClientSession) -> Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]]:
    async def inner(**kwargs: Any) -> tuple[Any, int, SimpleCookie]:
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"X-Request-Id": "12345"}
        else:
            kwargs["headers"]["X-Request-Id"] = "test_id"

        async with aio_session.patch(**kwargs) as response:
            body = await response.json()
            status = response.status
            cookies = response.cookies

        return body, status, cookies

    return inner


@pytest_asyncio.fixture(name="make_delete_request")
def make_delete_request(
    aio_session: ClientSession,
) -> Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]]:
    async def inner(**kwargs: Any) -> tuple[Any, int, SimpleCookie]:
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"X-Request-Id": "12345"}
        else:
            kwargs["headers"]["X-Request-Id"] = "test_id"

        async with aio_session.delete(**kwargs) as response:
            body = await response.json()
            status = response.status
            cookies = response.cookies

        return body, status, cookies

    return inner
