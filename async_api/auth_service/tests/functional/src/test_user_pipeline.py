import asyncio
from http import HTTPStatus

import pytest
from aiohttp import ClientSession, FormData
from tests.functional.settings import auth_test_settings


@pytest.mark.asyncio
async def test_signup(aiohttp_client1: ClientSession, random_creds: dict[str, str]):

    creds = {
        "login": random_creds["username"],
        "email": f'{random_creds["username"]}@example.com',
        "first_name": random_creds["username"],
        "last_name": random_creds["username"],
        "password": random_creds["password"]
    }

    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/signup",
        json=creds,
        )

    assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_login(aiohttp_client1: ClientSession, random_creds: dict[str, str]):
    data = FormData()
    data.add_field('username', random_creds["username"])
    data.add_field('password', random_creds["password"])

    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/login",
        data=data,
        )

    assert resp.status == HTTPStatus.OK
    assert resp.cookies.get("access_token", None) is not None
    assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_refresh_tokens(aiohttp_client1: ClientSession):
    old_access = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("access_token", None).value
    old_refresh = aiohttp_client1 \
        .cookie_jar \
        .filter_cookies("http://localhost") \
        .get("refresh_token", None).value

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
async def test_update_name(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users/me"
        )
    assert resp.status == HTTPStatus.OK
    old_user = await resp.json()

    user_update = {
        "first_name": "Tom"
    }
    resp = await aiohttp_client1.put(
        f"{auth_test_settings.root_path}/users",
        json=user_update,
        )
    assert resp.status == HTTPStatus.OK

    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users/me"
        )
    assert resp.status == HTTPStatus.OK
    new_user = await resp.json()

    assert new_user["first_name"] != old_user["first_name"]


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
