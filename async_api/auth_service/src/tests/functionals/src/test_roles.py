import pytest


@pytest.mark.asyncio
async def test_get_roles(client, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    print(response.json())
    assert response.status_code == 200
