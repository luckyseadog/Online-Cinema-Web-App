import pytest
from uuid import uuid4

ID_ROLE = str(uuid4())
test_role = {
    'id': ID_ROLE,
    'title': 'test role',
    'description': 'test role description',
}


@pytest.mark.asyncio
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

    response = await client.post(
        url='/admin/roles',
        json=test_role,
        cookies=cookies,
    )


@pytest.mark.asyncio
async def test_create_role(client, cookies):
    response = await client.post(
        url='/admin/roles',
        json=test_role,
        cookies=cookies,
    )
    assert response.status_code == 200
    assert response.json() == test_role


@pytest.mark.asyncio
async def test_update_role(client, cookies):
    response = await client.put(
        url='/admin/roles',
        json=test_role,
        cookies=cookies,
    )
    assert response.status_code == 404
    assert response.json() == {'detail': f'role with id {test_role["id"]} does not exist'}


@pytest.mark.asyncio
async def test_delete_role(client, cookies):
    response = await client.delete('/admin/roles')
    assert response.status_code == 200
