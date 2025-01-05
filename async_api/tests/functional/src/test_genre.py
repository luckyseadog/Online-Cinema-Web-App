from http import HTTPStatus

import pytest
from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'test_params', 
    [
        {"page_size": 1, "page_number": 0, "status_code": HTTPStatus.OK}, 
        {"page_size": 10, "page_number": 0, "status_code": HTTPStatus.OK},
        {"page_size": 1, "page_number": 100, "status_code": HTTPStatus.NOT_FOUND},
        {"page_size": -1, "page_number": 100, "status_code": HTTPStatus.UNPROCESSABLE_ENTITY},
        {"page_size": 1000, "page_number": 1000, "status_code": HTTPStatus.UNPROCESSABLE_ENTITY},
    ],
    ids=["One genre", "Many genres", "Out of bounds", "Page_size<0", "Page_size>100"]
)
@pytest.mark.asyncio
async def test_get_all_genres(test_params, aiohttp_client, es_write_data, event_loop):
    query_params = {'page_size': test_params["page_size"], 'page_number': test_params["page_number"]}

    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/genres',
        params=query_params
    ) as resp:
        assert resp.status == test_params["status_code"]
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert len(data) == test_params["page_size"]
            assert list(data[0]) == ["id", "name", "description"]

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ["detail"]

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ["detail"]


@pytest.mark.parametrize(
    'test_params', 
    [
        {
            "genre_id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395", 
            "name": "Short", 
            "status_code": HTTPStatus.OK,
        },
        {
            "genre_id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", 
            "name": "Romance", 
            "status_code": HTTPStatus.OK,
        },
        {
            "genre_id": "237fd1e4-c98e-454e-aa13-999999999999", 
            "name": "-", 
            "status_code": HTTPStatus.NOT_FOUND,
        },
        {
            "genre_id": "<notvalid>", 
            "name": "-", 
            "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    ],
    ids=["Short ID", "Romance ID", "Not existed ID", "Not valid ID"]
)
@pytest.mark.asyncio
async def test_get_genre_by_id(test_params, aiohttp_client, es_write_data, event_loop):

    async with aiohttp_client.get(
        f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/genres/{test_params["genre_id"]}'
    ) as resp:
        assert resp.status == test_params["status_code"]
        data = await resp.json()

        if resp.status == HTTPStatus.OK:
            assert data["name"] == test_params["name"]
            assert set(data.keys()) == set(["id", "name", "description"])

        elif resp.status == HTTPStatus.NOT_FOUND:
            assert list(data.keys()) == ["detail"]

        elif resp.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            assert list(data.keys()) == ["detail"]


@pytest.mark.parametrize(
    'params', 
    [
        {"page_size": None, "page_number": None},
        {"page_size": 10, "page_number": None},
        {"page_size": 20, "page_number": 0},
    ],

    ids=["WithoutQueries", "PageSize", "PageSize&PageNumber"]
)
@pytest.mark.asyncio
async def test_get_all_genres_cache(params, aiohttp_client, es_write_data, redis_client, event_loop):
    await redis_client.flushall()
    query_params = {key: value for key, value in params.items() if value is not None}
    cache_id = '_'.join(["genres", "get_all", str(params["page_size"] or 50), str(params["page_number"] or 0)])

    async with aiohttp_client.get(
            f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/genres',
            params=query_params,
        ) as resp:

        result = await redis_client.get(cache_id)
        assert result is not None