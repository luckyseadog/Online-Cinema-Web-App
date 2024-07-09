import pytest
from tests.functional.settings import auth_test_settings
from aiohttp import FormData

from faker import Faker

from uuid import uuid4

faker = Faker()


USER_NAME = faker.user_name()
USER_PASSWORD = faker.password()


@pytest.mark.asyncio
async def test_two_signup(aiohttp_client1):
    creds = {
        "login": USER_NAME,
        "email": f"{USER_NAME}@example.com",
        "first_name": USER_NAME,
        "last_name": USER_NAME,
        "password": USER_PASSWORD
    }

    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/signup", json=creds)

    assert resp.status == 200


@pytest.mark.asyncio
async def test_two_login(aiohttp_client1, aiohttp_client2):
    for client in [aiohttp_client1, aiohttp_client2]:
        data = FormData()
        data.add_field('username', USER_NAME)
        data.add_field('password', USER_PASSWORD)

        resp = await client.post(f"{auth_test_settings.root_path}/login", data=data)

        assert resp.status == 200
        assert resp.cookies.get("access_token", None) is not None
        assert resp.cookies.get("refresh_token", None) is not None

@pytest.mark.asyncio
async def test_two_logout_all(aiohttp_client1):
    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/logout_all")
    assert resp.status == 200

    assert aiohttp_client1.cookie_jar.filter_cookies("").get("access_token", None) is None
    assert aiohttp_client1.cookie_jar.filter_cookies("").get("refresh_token", None) is None

    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 401


@pytest.mark.asyncio
async def test_two_me(aiohttp_client2):
    resp = await aiohttp_client2.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 401


@pytest.mark.asyncio
async def test_two_refresh(aiohttp_client2):
    resp = await aiohttp_client2.post(f"{auth_test_settings.root_path}/refresh")
    assert resp.status == 403



