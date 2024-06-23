import pytest
from tests.settings import settings


@pytest.mark.asyncio
async def test_get_roles(client, prepare_database, fill_db):

    response = await client.post(
        '/login', data={
            'username': 'superadmin',
            'password': 'superadmin',
        },
        headers={'Origin': settings.root_path},
    )
    print('superadmin', fill_db)

    print(response.json())
    print(response.cookies)

    # response = await client.get('/admin/roles/roles')
    # print(response.json())
    # assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role(client):
    response = await client.get('/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_role(client):
    response = await client.get('/admin/roles')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_role(client):
    response = await client.get('/admin/roles')
    assert response.status_code == 200
