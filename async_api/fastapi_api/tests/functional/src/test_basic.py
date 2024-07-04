import pytest


@pytest.mark.parametrize(
    'index, answer', [('movies', 100), ('genres', 26), ('persons', 400)],
)
@pytest.mark.asyncio
async def test_basic(index, answer, aiohttp_client, es_write_data, event_loop, es_client):
    resp = await es_client.count(index=index)

    assert resp['count'] == answer
