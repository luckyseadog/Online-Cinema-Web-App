import pytest
from tests.functional.settings import auth_test_settings
import asyncio



@pytest.mark.asyncio
async def test_guest_signup(aiohttp_client1):
    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/signup_guest")

    assert resp.status == 200
    assert resp.cookies.get("access_token", None) is not None
    assert resp.cookies.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_guest_refresh(aiohttp_client1):
    old_access = aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("access_token", None)
    old_refresh = aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("refresh_token", None)

    await asyncio.sleep(1)
    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/refresh")
    assert resp.status == 200

    new_access = aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("access_token", None).value
    new_refresh = aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("refresh_token", None).value

    assert new_access != old_access
    assert new_refresh != old_refresh


@pytest.mark.asyncio
async def test_guest_me(aiohttp_client1):
    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 200

    user = await resp.json()
    assert user["login"].startswith("guest")
    assert user["roles"][0]["title"] == "guest"


@pytest.mark.asyncio
async def test_guest_logout(aiohttp_client1):
    resp = await aiohttp_client1.post(f"{auth_test_settings.root_path}/logout")
    assert resp.status == 200

    assert aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("access_token", None) is None
    assert aiohttp_client1.cookie_jar.filter_cookies("http://localhost").get("refresh_token", None) is None

    resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/users/me")
    assert resp.status == 401


    

