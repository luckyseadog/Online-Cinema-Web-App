import pytest
# from httpx import codes
# from faker import Faker
from tests.settings import settings
# import json

test_user = {
    # 'login': 'test',
    # 'password': 'test',
    # 'email': 'test@example.com',
    # 'first_name': 'first_name',
    # 'last_name': 'last_name'

    'login': 'string',
    'email': 'string',
    'first_name': 'string',
    'last_name': 'string',
    'password': 'string',
}


@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post(
        url='/signup',
        data=test_user,
        # headers={'Origin': settings.root_path }
    )
    print(settings)
    print(response.json())
    assert response.status_code == 200
    assert 1 == 1
