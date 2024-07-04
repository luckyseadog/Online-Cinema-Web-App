import time
from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'test_params',
    [
        {'page_size': 1, 'page_number': 1, 'status_code': HTTPStatus.OK},
        {'page_size': 10, 'page_number': 1, 'status_code': HTTPStatus.OK},
        {'page_size': 1, 'page_number': 100, 'status_code': HTTPStatus.NOT_FOUND},
        {'page_size': -1, 'page_number': 100, 'status_code': HTTPStatus.UNPROCESSABLE_ENTITY},
        {'page_size': 1000, 'page_number': 1000, 'status_code': HTTPStatus.UNPROCESSABLE_ENTITY},
    ],
    ids=['One film', 'Many films', 'Out of bounds', 'Page_size<0', 'Page_size>100'],
)
@pytest.mark.asyncio
async def test_get_all_films(test_params, aiohttp_client, es_write_data, event_loop):
    query_params = {'page_size': test_params['page_size'], 'page_number': test_params['page_number']}

    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films',
        params=query_params,
    ) as resp:
        assert resp.status == test_params['status_code']
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert len(data) == test_params['page_size']

            mr = 10.0
            for film in data:
                assert film['imdb_rating'] <= mr
                mr = film['imdb_rating']

                assert list(film.keys()) == ['id', 'title', 'imdb_rating']

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ['detail']

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ['detail']


@pytest.mark.parametrize(
    'test_params',
    [
        {'page_size': 99, 'genre': 'Sport', 'count': 1, 'status_code': HTTPStatus.OK},
        {'page_size': 99, 'genre': 'Biography', 'count': 2, 'status_code': HTTPStatus.OK},
        {'page_size': 99, 'genre': 'NotGenre', 'status_code': HTTPStatus.NOT_FOUND},
        {'page_size': 1000, 'genre': 'NotGenre', 'status_code': HTTPStatus.UNPROCESSABLE_ENTITY},
    ],
    ids=['Adventure genre', 'Biography genre', 'Non-existed Genre', 'Page_size>100'],
)
@pytest.mark.asyncio
async def test_get_all_films_with_genres(test_params, aiohttp_client, es_write_data, event_loop):
    query_params = {
        'page_size': test_params['page_size'],
        'genre': test_params['genre'],
        'sort': '-imdb_rating',
    }

    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films',
        params=query_params,
    ) as resp:
        assert resp.status == test_params['status_code']
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert len(data) == test_params['count']

            mr = 10.0
            for film in data:
                assert film['imdb_rating'] <= mr
                mr = film['imdb_rating']

                assert list(film.keys()) == ['id', 'title', 'imdb_rating']

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ['detail']

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ['detail']


@pytest.mark.parametrize(
    'test_params',
    [
        {
            'film_id': 'b1384a92-f7fe-476b-b90b-6cec2b7a0dce',
            'title': 'Star Trek: The Next Generation',
            'status_code': HTTPStatus.OK,
        },
        {
            'film_id': 'a72e0406-8b09-4f7a-9d2b-cd261c2729f4',
            'title': 'Lone Star Justice',
            'status_code': HTTPStatus.OK,
        },
        {
            'film_id': 'a72e0406-8b09-4f7a-9d2b-999999999999',
            'title': '-',
            'status_code': HTTPStatus.NOT_FOUND,
        },
        {
            'film_id': '<notvalid>',
            'title': '-',
            'status_code': HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    ],
    ids=['Star Trek ID', 'Lone Star Justice ID', 'Not existed ID', 'Not valid ID'],
)
@pytest.mark.asyncio
async def test_get_film_by_id(test_params, aiohttp_client, es_write_data, event_loop):

    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films/{test_params["film_id"]}',
    ) as resp:
        assert resp.status == test_params['status_code']
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert data['title'] == test_params['title']
            assert set(data.keys()) == {
                'id', 'title', 'imdb_rating', 'description',
                'genre', 'actors', 'writers', 'directors',
            }

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ['detail']

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ['detail']


@pytest.mark.parametrize(
    'params',
    [
        {'page_size': None, 'page_number': None, 'genre': None},
        {'page_size': 10, 'page_number': None, 'genre': None},
        {'page_size': 20, 'page_number': 0, 'genre': 'Drama'},
    ],

    ids=['WithoutQueries', 'PageSize', 'Genre&PageSize&PageNumber'],
)
@pytest.mark.asyncio
async def test_get_all_films_cache(params, aiohttp_client, es_write_data, redis_client, event_loop):
    await redis_client.flushall()
    query_params = {key: value for key, value in params.items() if value is not None}
    cache_id = '_'.join([
        'movies', 'get_all_films', str(params['page_size'] or 50), str(
            params['page_number'] or 0,
        ), str(params['genre']), 'SortModel.descending',
    ])

    async with aiohttp_client.get(
            f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/films',
            params=query_params,
    ) as _:

        result = await redis_client.get(cache_id)
        assert result is not None


@pytest.mark.parametrize(
    'path',
    [
        '/api/v1/films?page_size=99',
        '/api/v1/films?sort=imdb_rating',
        '/api/v1/films?page_size=89&genre=Adventure',
    ],

    ids=['PageSize', 'Sort', 'PageSize&Genre'],
)
@pytest.mark.asyncio
async def test_get_all_films_cache_time(path, aiohttp_client, es_write_data, redis_client, event_loop):
    NUM_ITERS = 10**2
    await redis_client.flushall()

    t1_es = time.perf_counter()
    async with aiohttp_client.get(
            f'http://{test_settings.service_host}:{test_settings.service_port}{path}',
    ) as _:
        t2_es = time.perf_counter()

    es_time = t2_es - t1_es

    redis_time = 0.0
    for _ in range(NUM_ITERS):

        t1_cache = time.perf_counter()
        async with aiohttp_client.get(
                f'http://{test_settings.service_host}:{test_settings.service_port}{path}',
        ) as _:
            t2_cache = time.perf_counter()
            redis_time += t2_cache - t1_cache

    redis_time /= NUM_ITERS

    assert redis_time < es_time
