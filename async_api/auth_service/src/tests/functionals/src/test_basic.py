import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_basic_login(client, event_loop):
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await client.get("/api/v1/auth/users/history")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_admin(event_loop):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/admin/roles")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_auth(event_loop):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/users/access")
        assert response.status_code == 200
