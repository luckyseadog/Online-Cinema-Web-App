import asyncio
from http import HTTPStatus

import pytest
from aiohttp import ClientSession
from tests.functional.settings import auth_test_settings


@pytest.mark.asyncio
async def test_signup(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/signup_guest"
    )

    assert resp.status == HTTPStatus.OK
    assert resp.cookies.get("access_token", None) is not None
    assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_refresh(aiohttp_client1: ClientSession):
    old_access = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("access_token", None)
    old_refresh = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("refresh_token", None)

    await asyncio.sleep(1)
    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/refresh"
    )
    assert resp.status == HTTPStatus.OK

    new_access = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("access_token", None).value
    new_refresh = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("refresh_token", None).value

    assert new_access != old_access
    assert new_refresh != old_refresh


@pytest.mark.asyncio
async def test_getme(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users/me"
        )
    assert resp.status == HTTPStatus.OK

    user = await resp.json()
    assert user["login"].startswith("guest")
    assert user["roles"][0]["title"] == "guest"


@pytest.mark.asyncio
async def test_logout(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/logout"
        )
    assert resp.status == HTTPStatus.OK

    assert aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("access_token", None) is None
    assert aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("refresh_token", None) is None

    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users/me"
        )
    assert resp.status == HTTPStatus.UNAUTHORIZED
