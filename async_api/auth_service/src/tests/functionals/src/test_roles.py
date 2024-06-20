import pytest


@pytest.mark.asyncio
async def test_get_roles(client, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role(client, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_role(client, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_role(client, prepare_database):
    response = await client.get('/api/v1/auth/admin/roles')
    assert response.status_code == 200
