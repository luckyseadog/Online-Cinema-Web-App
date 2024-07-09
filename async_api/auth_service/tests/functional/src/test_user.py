import pytest
from tests.functional.settings import auth_test_settings
from aiohttp import FormData

from faker import Faker

from uuid import uuid4

faker = Faker()


USER_NAME = faker.user_name()
USER_PASSWORD = faker.password()



@pytest.mark.asyncio
async def test_user_signup(aiohttp_client1):
    # data = FormData()
    # data.add_field('username', 'superadmin')
    # data.add_field('password', 'admin')

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
async def test_user_login(aiohttp_client1):
    data = FormData()
    data.add_field('username', USER_NAME)
    data.add_field('password', USER_PASSWORD)

    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/login", data=data)

    assert resp.status == 200
    assert resp.cookies.get("access_token", None) is not None
    assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_user_refresh(aiohttp_client1):
    old_access = aiohttp_client1.cookie_jar.filter_cookies("").get("access_token", None)
    old_refresh = aiohttp_client1.cookie_jar.filter_cookies("").get("refresh_token", None)

    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/refresh")

    assert resp.status == 200
    assert resp.cookies["access_token"] != old_access
    assert resp.cookies["refresh_token"] != old_refresh


@pytest.mark.asyncio
async def test_user_update(aiohttp_client1):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 200
    old_user = await resp.json()


    user_update = {
        "first_name": "Tom"
    }
    resp = await aiohttp_client1.put(f"{auth_test_settings.root_path}/users", json=user_update)
    assert resp.status == 200

    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 200
    new_user = await resp.json()

    assert new_user["first_name"] != old_user["first_name"]


@pytest.mark.asyncio
async def test_user_logout(aiohttp_client1):
    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/logout")
    assert resp.status == 200

    assert aiohttp_client1.cookie_jar.filter_cookies("").get("access_token", None) is None
    assert aiohttp_client1.cookie_jar.filter_cookies("").get("refresh_token", None) is None

    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 401




