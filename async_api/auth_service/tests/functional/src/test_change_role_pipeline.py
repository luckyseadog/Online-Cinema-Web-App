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
        "password": random_creds["password"],
    }

    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/signup",
        json=creds
    )

    assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_login(aiohttp_client1: ClientSession, aiohttp_client2: ClientSession, random_creds: dict[str, str]):
    creds = [
        {
            "login": random_creds["username"],
            "password": random_creds["password"],
        },
        {
            "login": "superadmin",
            "password": "admin",
        },
    ]

    for client, cred in [(aiohttp_client1, creds[0]), (aiohttp_client2, creds[1])]:
        data = FormData()
        data.add_field('username', cred["login"])
        data.add_field('password', cred["password"])

        resp = await client.post(
            f"{auth_test_settings.root_path}/login",
            data=data
        )

        assert resp.status == HTTPStatus.OK
        assert resp.cookies.get("access_token", None) is not None
        assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_no_access(aiohttp_client1: ClientSession):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users"
    )
    assert resp.status == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_add_admin_role(aiohttp_client1: ClientSession, aiohttp_client2: ClientSession):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users/me"
    )
    assert resp.status == HTTPStatus.OK

    user = await resp.json()
    user_id = user["id"]

    resp = await aiohttp_client2.get(
        f"{auth_test_settings.root_path}/admin/roles"
    )
    assert resp.status == HTTPStatus.OK

    roles = await resp.json()
    for role in roles:
        if role["title"] == "admin":
            role_id = role["id"]

    body = {
        "role_id": role_id,
        "user_id": user_id,
    }
    resp = await aiohttp_client2.post(
        f"{auth_test_settings.root_path}/admin/user_role/assign",
        json=body
    )
    assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_access(aiohttp_client1):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/users"
    )
    assert resp.status == HTTPStatus.OK
