# все граничные случаи по валидации данных;
# поиск конкретного человека;
# поиск всех фильмов с участием человека;
# вывести всех людей;
# поиск с учётом кеша в Redis.
import json
import uuid
from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings

BASE_URL = f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/persons'
@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'page_number': 0, 'page_size': 50},
            {'status': HTTPStatus.OK, 'length': 50},
        ),
        (
            {'page_number': 1, 'page_size': 50},
            {'status': HTTPStatus.OK, 'length': 50},
        ),
        (
            {'page_number': 2, 'page_size': 50},
            {'status': HTTPStatus.OK, 'length': 50},
        ),
        (
            {'page_number': 7, 'page_size': 50},
            {'status': HTTPStatus.OK, 'length': 50},
        ),
        (
            {'page_number': 0, 'page_size': 10},
            {'status': HTTPStatus.OK, 'length': 10},
        ),
        (
            {'page_number': 4, 'page_size': 99},
            {'status': HTTPStatus.OK, 'length': 4},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_all_persons(make_request, es_write_data, params, expected_answer):
    response = await make_request(BASE_URL, params)
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'},
            {
                'status': HTTPStatus.OK,
                'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358',
                'name': 'Carrie Fisher',
            },
        ),
        (
            {'id': '62df10e8-244d-4c31-b396-564dfbc2f9c5'},
            {
                'status': HTTPStatus.OK,
                'id': '62df10e8-244d-4c31-b396-564dfbc2f9c5',
                'name': 'Hayden Christensen',
            },
        ),
        (
            {'id': '189f1d17-c928-492a-aa33-2212b5ad1555'},
            {
                'status': HTTPStatus.OK,
                'id': '189f1d17-c928-492a-aa33-2212b5ad1555',
                'name': 'Gareth Edwards',
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_person_by_id(make_request, es_write_data, params, answer):
    response = await make_request(f'{BASE_URL}/{params["id"]}')

    assert response.status == answer['status']
    assert response.body['id'] == answer['id']
    assert response.body['name'] == answer['name']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'id': uuid.uuid4()},
            {'description': {'detail': 'person not found'}},
        ),
        (
            {'id': uuid.uuid4()},
            {'description': {'detail': 'person not found'}},
        ),
        (
            {'id': uuid.uuid4()},
            {'description': {'detail': 'person not found'}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_person_by_id_not_found(make_request, es_write_data, params, answer):
    response = await make_request(f'{BASE_URL}/{params["id"]}')
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body == answer['description']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'page_number': 8, 'page_size': 50},
            {'status': HTTPStatus.NOT_FOUND, 'description': {'detail': 'not found persons'}},
        ),
        (
            {'page_number': 21, 'page_size': 20},
            {'status': HTTPStatus.NOT_FOUND, 'description': {'detail': 'not found persons'}},
        ),
        (
            {'page_number': 401, 'page_size': 1},
            {'status': HTTPStatus.NOT_FOUND, 'description': {'detail': 'not found persons'}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_all_persons_wrong_page_number(make_request, es_write_data, params, answer):
    response = await make_request(BASE_URL, params)
    assert response.status == answer['status']
    assert response.body == answer['description']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'page_number': 0, 'page_size': 0},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'description': 'Input should be greater than 0'},

        ),
        (
            {'page_number': -1, 'page_size': 0},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'description': 'Input should be greater than 0'},

        ),
        (
            {'page_number': 1, 'page_size': 100},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'description': 'Input should be less than 100'},

        ),
    ],
)
@pytest.mark.asyncio
async def test_get_all_persons_validation_error(make_request, es_write_data, params, answer):
    response = await make_request(BASE_URL, params)
    assert response.status == answer['status']
    assert response.body['detail'][0]['msg'] == answer['description']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'},
            {'status': HTTPStatus.OK, 'len_films': 4},

        ),
        (
            {'id': 'ed149438-4d76-45c9-861b-d3ed48ccbf0c'},
            {'status': HTTPStatus.OK, 'len_films': 1},

        ),
        (
            {'id': 'efdd1787-8871-4aa9-b1d7-f68e55b913ed'},
            {'status': HTTPStatus.OK, 'len_films': 3},

        ),
    ],
)
@pytest.mark.asyncio
async def test_get_person_films(make_request, es_write_data, params, answer):
    response = await make_request(f'{BASE_URL}/{params["id"]}/films')
    # response2 = await make_request(f'{BASE_URL}/{params["id"]}')
    # print(response.body['films'])
    assert response.status == answer['status']
    # assert response2.status == answer['status']
    # assert len(response.body) == answer['len_films']
    # assert len(response2.body['films']) == answer['len_films']
    # for i in range(0, len(response1.body)):
    #     assert response1.body[i]['id'] == response2.body['films'][i]['id']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'id': 'f24f3fa4-2e42-4dde-be8c-2aba541a593b'},
            {'len_films': 0},

        ),
        (
            {'id': '2b0f84fb-416b-4c30-80db-69478bf872be'},
            {'len_films': 0},

        ),
        (
            {'id': '7fb9ae3d-aeac-40a9-aa25-cd6992be16a6'},
            {'len_films': 0},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_person_films_not_found(make_request, es_write_data, params, answer):
    response1 = await make_request(f'{BASE_URL}/{params["id"]}/films')
    response2 = await make_request(f'{BASE_URL}/{params["id"]}')

    assert response1.status == HTTPStatus.NOT_FOUND
    assert response2.status == HTTPStatus.OK
    assert len(response2.body['films']) == answer['len_films']

@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358'},
            {
                'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358',
                'name': 'Carrie Fisher',
            },

        ),
        (
            {'id': 'ed149438-4d76-45c9-861b-d3ed48ccbf0c'},
            {
                'id': 'ed149438-4d76-45c9-861b-d3ed48ccbf0c',
                'name': 'Leigh Brackett',
            },
        ),
        (
            {'id': 'efdd1787-8871-4aa9-b1d7-f68e55b913ed'},
            {
                'id': 'efdd1787-8871-4aa9-b1d7-f68e55b913ed',
                'name': 'Billy Dee Williams',
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_get_person_by_id_from_cache(make_request, es_write_data, redis_client, params, answer):
    await redis_client.flushall()
    response = await make_request(f'{BASE_URL}/{params["id"]}')
    assert response.status == HTTPStatus.OK
    assert response.body['id'] == answer['id']

    res = json.loads(await redis_client.get('_'.join(['persons', 'get_by_id', params['id']])))

    assert res['id'] == answer['id']
    assert res['name'] == answer['name']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'page_size': 50, 'page_number': 1},
            {'length': 50},
        ),
        (
            {'page_size': 25, 'page_number': 1},
            {'length': 25},
        ),
        (
            {'page_size': 93, 'page_number': 4},
            {'length': 28},
        ),
        (
            {'page_size': 99, 'page_number': 4},
            {'length': 4},
        ),

    ],
)
@pytest.mark.asyncio
async def test_get_all_persons_from_cache(make_request, es_write_data, redis_client, params, answer):
    await redis_client.flushall()
    response = await make_request(BASE_URL, params)
    assert response.status == HTTPStatus.OK

    res = await redis_client.get('_'.join(['persons', str(params['page_size']), str(params['page_number'])]))

    assert res is not None
    assert len(res.split(sep=b'<delimiter>')) == answer['length']
