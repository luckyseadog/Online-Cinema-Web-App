import pytest
from httpx import codes

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        'http://localhost:8000/api/v1/auth/signup',
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
    assert response.status_code == codes.CREATED

    assert len(response.json()) == 4
