import pytest
from tests.functional.settings import auth_test_settings
from aiohttp import FormData
import pdb 
import asyncio

from faker import Faker

from uuid import uuid4

faker = Faker()


USER_NAME = faker.user_name()
USER_PASSWORD = faker.password()


# pdb.set_trace()


@pytest.mark.asyncio
async def test_user_signup(aiohttp_client1):
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
async def test_delete_login(aiohttp_client1, aiohttp_client2):
    for client in [aiohttp_client1, aiohttp_client2]:
        data = FormData()
        data.add_field('username', USER_NAME)
        data.add_field('password', USER_PASSWORD)

        resp = await client.post(f"{auth_test_settings.root_path}/login", data=data)

        assert resp.status == 200

        assert client.cookie_jar.filter_cookies("http://localhost").get("access_token", None) is not None
        assert client.cookie_jar.filter_cookies("http://localhost").get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_delete_delete(aiohttp_client1, aiohttp_client2):
    resp = await aiohttp_client2.delete(f"{auth_test_settings.root_path}/users")
    assert resp.status == 200

    assert aiohttp_client2.cookie_jar.filter_cookies("http://localhost").get("access_token", None) is None
    assert aiohttp_client2.cookie_jar.filter_cookies("http://localhost").get("refresh_token", None) is None


@pytest.mark.asyncio
async def test_delete_me(aiohttp_client1):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 401

    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/refresh")
    assert resp.status == 403


@pytest.mark.asyncio
async def test_delete_login2(aiohttp_client2):
    data = FormData()
    data.add_field('username', USER_NAME)
    data.add_field('password', USER_PASSWORD)

    resp = await aiohttp_client2.post(f"{auth_test_settings.root_path}/login", data=data)

    assert resp.status == 400


