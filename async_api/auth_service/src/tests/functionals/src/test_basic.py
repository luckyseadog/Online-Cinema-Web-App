import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_database(client: AsyncClient):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200
    assert len(response.json()) == 4
