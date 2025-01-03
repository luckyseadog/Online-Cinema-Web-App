from http import HTTPStatus
from typing import Callable

import pytest
from aiohttp import ClientSession, FormData
from tests.functional.settings import auth_test_settings


@pytest.mark.asyncio
async def test_login(aiohttp_client1: ClientSession, role_count: Callable[[], int]):
    data = FormData()
    data.add_field('username', "superadmin")
    data.add_field('password', "admin")

    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/login",
        data=data
    )

    assert resp.status == HTTPStatus.OK
    assert resp.cookies.get("access_token", None) is not None
    assert resp.cookies.get("refresh_token", None) is not None
    assert await role_count() == 5


@pytest.mark.asyncio
async def test_role_add(aiohttp_client1: ClientSession, role_count: Callable[[], int]):
    role_create = {
        "title": "test role",
        "description": "test role description"
    }

    resp = await aiohttp_client1.post(
        f"{auth_test_settings.root_path}/admin/roles",
        json=role_create
    )
    assert resp.status == HTTPStatus.OK
    assert await role_count() == 6


@pytest.mark.asyncio
async def test_role_delete(aiohttp_client1: ClientSession, role_count: Callable[[], int]):
    resp = await aiohttp_client1.get(
        f"{auth_test_settings.root_path}/admin/roles"
    )
    assert resp.status == HTTPStatus.OK

    roles = await resp.json()
    role_id = None
    for role in roles:
        if role["title"] == "test role":
            role_id = role["id"]

    params = {"role_id": role_id}
    resp = await aiohttp_client1.delete(
        f"{auth_test_settings.root_path}/admin/roles",
        params=params
    )
    assert resp.status == HTTPStatus.OK
    assert await role_count() == 5
