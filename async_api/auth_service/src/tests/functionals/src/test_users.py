import pytest


@pytest.mark.asyncio
async def test_get_users(client):
    response = await client.get('/users/users')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        '/signup',
        headers={'Origin': 'http://localhost:8000'},
        json={
            'login': 'test23',
            'password': 'password',
            'first_name': 'test23',
            'last_name': 'test23',
            'email': 'test23@example.com',
        },
    )
    print(response.json())
    print(response.headers)
    print(response.cookies)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login(client):
    pass

@pytest.mark.asyncio
async def test_logout(client):
    response = await client.post('/logout')
    assert response.status_code == 401
