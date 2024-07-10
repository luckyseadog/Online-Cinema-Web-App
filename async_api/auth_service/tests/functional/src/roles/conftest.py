import asyncio

import aiohttp
import pytest_asyncio
from redis.asyncio import Redis
from collections.abc import AsyncGenerator
from tests.functional.settings import auth_test_settings
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, AsyncEngine, AsyncConnection,
)
from tests.functional.utils.db_models import Base
from pathlib import Path
from faker import Faker

@pytest_asyncio.fixture(scope='module')
async def role_count(aiohttp_client1, aiohttp_client2):
    async def inner():
        resp = await aiohttp_client1.get(f"{auth_test_settings.root_path}/admin/roles")
        assert resp.status == 200
        roles = await resp.json()
        return len(roles)
    return inner