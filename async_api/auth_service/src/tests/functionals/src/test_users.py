import pytest
from httpx import codes
from faker import Faker

from tests.settings import settings

# @pytest.mark.asyncio
# async def test_get_users(client):
#     response = await client.get('/users')
#     assert response.status_code == 401
faker = Faker()

my_test_user = {
    'login': faker.user_name(),
    'password': faker.password(),
    'first_name': faker.first_name(),
    'last_name': faker.last_name(),
    'email': faker.email(),
}


@pytest.mark.asyncio
async def test_test(prepare_database, client):
    response = await client.get('/login')
    # print(response.status_code)
    # print(response.json())
    print(response.json())

    assert 1 == 1


@pytest.mark.asyncio
async def test_create_user(prepare_database, client):
    response = await client.post(
        url='/signup',
        headers={'Origin': settings.root_path},
        json=my_test_user,
    )
    print(settings)
    assert response.status_code == codes.OK
    assert response.json()['message'] == 'User created successfully'


@pytest.mark.asyncio
async def test_login(client, prepare_database):
    response = await client.post(
        '/login',
        headers={'Origin': settings.root_path},
        data={
            'username': my_test_user['login'],
            'password': my_test_user['password'],
        },
    )
    print(response.headers)
    print(response.json())

    assert response.status_code == codes.OK

@pytest.mark.asyncio
async def test_logout(client):
    response = await client.post('/logout')
    assert response.status_code == 401
