from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings

BASE_PERSON_URL = f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/persons/search'


@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'query': r'pirates%20of%20the%20caribbean'},
            {'status_code': HTTPStatus.NOT_FOUND, 'length': -1},
        ),
        (
            {'query': r'star%20wars'},
            {'status_code': HTTPStatus.OK, 'length': 50},
        ),
        (
            {'query': r'the%20secret%20world%20of%20jeffree'},
            {'status_code': HTTPStatus.OK, 'length': 1},
        ),
    ],
    ids=["No match", "All match", "Single match"]
)
@pytest.mark.asyncio
async def test_search_films(
    params,
    expected_answer,
    es_client,
    es_write_data,
    event_loop,
    aiohttp_client,
):
    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films/search/?query={params["query"]}'
    ) as resp:
        assert resp.status == expected_answer["status_code"]
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert len(data) ==  expected_answer["length"]

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ["detail"]

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ["detail"]


@pytest.mark.parametrize(
    'params', 
    [
        {"page_size": None, "page_number": None, "query": r"blazers%202199"},
        {"page_size": 10, "page_number": None, "query": r"elevator%20prank"},
        {"page_size": 20, "page_number": 0,"query": r"birth%20of%20the%20federation"},
    ],

    ids=["QueryOnly", "Query&PageSize", "Query&PageSize"]
)
@pytest.mark.asyncio
async def test_search_films_cache(params, aiohttp_client, es_write_data, redis_client, event_loop):
    await redis_client.flushall()
    query_params = {key: value for key, value in params.items() if value is not None}
    cache_id = "_".join(["movies", "film_search", str(params["query"]), str(params["page_size"] or 50), str(params["page_number"] or 0)])

    async with aiohttp_client.get(
            f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films/search',
            params=query_params,
        ) as resp:

        result = await redis_client.get(cache_id)
        assert result is not None



@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'query': 'george'},
            {'length': 3},
        ),
        (
            {'query': 'piter'},
            {'length': 4},
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(
        es_client,
        es_write_data,
        event_loop,
        aiohttp_client,
        make_request,
        params,
        answer,
):
    resp = await make_request(BASE_PERSON_URL, params)
    assert resp.status == HTTPStatus.OK
    assert len(resp.body) == answer['length']


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {'query': 'unknown'},
            {'length': 1},
        ),
        (
            {'query': 'fedya'},
            {'length': 1},
        ),
        (
            {'query': 'Фёдор'},
            {'length': 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons_not_found(
        es_client,
        es_write_data,
        event_loop,
        aiohttp_client,
        make_request,
        params,
        answer,
):
    resp = await make_request(BASE_PERSON_URL, params)

    assert resp.status == HTTPStatus.NOT_FOUND
    assert len(resp.body) == answer['length']
    assert resp.body == {'detail': f'not found persons by key: {params["query"]}'}


@pytest.mark.parametrize(
    'params, answer',
    [
        (
            {},
            {'length': 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons_unprocessable_entity(
        es_client,
        es_write_data,
        event_loop,
        aiohttp_client,
        make_request,
        params,
        answer,
):
    resp = await make_request(BASE_PERSON_URL, params)

    assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(resp.body) == answer['length']
    assert resp.body['detail'][0]['msg'] == 'Field required'
