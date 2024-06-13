import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_basic_users(client: AsyncClient):
    response = await client.get('/api/v1/auth/users/users')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_admin(client: AsyncClient):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_auth(client: AsyncClient):
    response = await client.get('/api/v1/auth/')
    assert response.status_code == 200
