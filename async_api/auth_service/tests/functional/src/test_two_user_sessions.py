from http import HTTPStatus

import pytest
from aiohttp import ClientSession, FormData
from tests.functional.settings import auth_test_settings


@pytest.mark.asyncio
async def test_signup(aiohttp_client1: ClientSession, random_creds):
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
async def test_login(aiohttp_client1: ClientSession, aiohttp_client2: ClientSession, random_creds: dict[str, str]):
    for client in [aiohttp_client1, aiohttp_client2]:
        data = FormData()
        data.add_field('username', random_creds["username"])
        data.add_field('password', random_creds["password"])

        resp = await client.post(
            f"{auth_test_settings.root_path}/login", 
            data=data
            )

        assert resp.status == HTTPStatus.OK
        assert resp.cookies.get("access_token", None) is not None
        assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_logout_all_session1(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/logout_all"
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


@pytest.mark.asyncio
async def test_getme_session2(aiohttp_client2: ClientSession):
    resp = await aiohttp_client2.get(
        f"{auth_test_settings.root_path}/users/me"
        )
    assert resp.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_session(aiohttp_client2: ClientSession):
    resp = await aiohttp_client2.post(
        f"{auth_test_settings.root_path}/refresh"
        )
    assert resp.status == HTTPStatus.FORBIDDEN
