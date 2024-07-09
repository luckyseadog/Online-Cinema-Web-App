import pytest
from tests.functional.settings import auth_test_settings
from aiohttp import FormData
from faker import Faker

from uuid import uuid4

faker = Faker()


USER_NAME = faker.user_name()
USER_PASSWORD = faker.password()



@pytest.mark.asyncio
async def test_change_signup(aiohttp_client1):
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
async def test_change_login(aiohttp_client1, aiohttp_client2):
    creds = [
        {"login": USER_NAME, "password": USER_PASSWORD},
        {"login": "superadmin", "password": "admin"},
    ]

    for client, cred in [(aiohttp_client1, creds[0]), (aiohttp_client2, creds[1])]:
        data = FormData()
        data.add_field('username', cred["login"])
        data.add_field('password', cred["password"])

        resp = await client.post(f"{auth_test_settings.root_path}/login", data=data)

        assert resp.status == 200
        assert resp.cookies.get("access_token", None) is not None
        assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_change_users_1(aiohttp_client1):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users")
    assert resp.status == 403


@pytest.mark.asyncio
async def test_change_assign(aiohttp_client1, aiohttp_client2):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 200

    user = await resp.json()
    user_id = user["id"]

    resp = await aiohttp_client2.get(f"{auth_test_settings.root_path}/admin/roles")
    assert resp.status == 200

    roles = await resp.json()
    for role in roles:
        if role["title"] == "admin":
            role_id = role["id"]

    body = {
        "role_id": role_id,
        "user_id": user_id
    }
    resp = await aiohttp_client2.post(f"{auth_test_settings.root_path}/admin/user_role/assign", json=body)
    assert resp.status == 200


@pytest.mark.asyncio
async def test_change_users_2(aiohttp_client1):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users")
    assert resp.status == 200

    

    
