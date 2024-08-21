import pytest_asyncio
from tests.functional.settings import auth_test_settings


@pytest_asyncio.fixture(scope='module')
async def role_count(aiohttp_client1, aiohttp_client2):
    async def inner():
        resp = await aiohttp_client1.get(
            f"{auth_test_settings.root_path}/admin/roles"
        )
        assert resp.status == 200
        roles = await resp.json()
        return len(roles)
    return inner
