import pytest


@pytest.mark.asyncio
# async def test_get_roles(client, prepare_database, fill_db, cookies):
async def test_get_roles(client, cookies):
    response = await client.get(
        '/admin/roles',
        cookies=cookies,
    )
    roles = response.json()
    list_roles = [item['title'] for item in roles]
    assert len(roles) == 5
    assert 'superadmin' in list_roles
    assert 'admin' in list_roles
    assert 'user' in list_roles
    assert 'guest' in list_roles
    assert 'subscriber' in list_roles
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role(client, cookies):
    response = await client.post('/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_role(client, cookies):
    response = await client.put('/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_role(client, cookies):
    response = await client.delete('/admin/roles')
    assert response.status_code == 200
