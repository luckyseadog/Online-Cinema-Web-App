import pytest
from httpx import codes


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {
                'url': '/admin/roles/roles',
                'method': 'GET',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/admin/roles/roles',
                'method': 'PUT',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/admin/roles/roles',
                'method': 'POST',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/admin/roles/roles',
                'method': 'DELETE',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/users/users',
                'method': 'GET',
            },
            {'status': codes.UNAUTHORIZED},
        ),

        (
            {
                'url': '/users/',
                'method': 'PUT',
            },
            {'status': codes.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                'url': '/users/',
                'method': 'DELETE',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/users/me',
                'method': 'GET',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/users/history',
                'method': 'GET',
            },
            {'status': codes.UNAUTHORIZED},
        ),
        (
            {
                'url': '/logout',
                'method': 'POST',
            },
            {'status': codes.UNAUTHORIZED},
        ),
    ],
    ids=[
        'GET /roles',
        'POST /roles',
        'PUT /roles',
        'DELETE /roles',
        'GET /users',
        'PUT /users',
        'DELETE /users',
        'GET /users/me',
        'GET /users/history',
        'POST /logout',
    ],
)
@pytest.mark.asyncio
async def test_protected_handlers(params, answer, client):
    data = {
        'GET': client.get,
        'POST': client.post,
        'PUT': client.put,
        'DELETE': client.delete,
    }
    response = await data[params['method']](params['url'])
    assert response.status_code == answer['status']
