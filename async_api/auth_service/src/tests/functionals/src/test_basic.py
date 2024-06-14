import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_database(client: AsyncClient, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    print('=' * 100)
    print(response.json())
    print('=' * 100)
    assert response.status_code == 200
