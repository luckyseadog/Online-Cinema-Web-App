import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import aiohttp
import pytest_asyncio
from faker import Faker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    create_async_engine)
from tests.functional.settings import auth_test_settings
from tests.functional.utils.db_models import Base


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def aiohttp_client1():
    headers = {"Origin": "www.somesite.com"}
    jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(
        cookie_jar=jar,
        headers=headers
    )

    yield session

    await session.close()


@pytest_asyncio.fixture(scope='module')
async def aiohttp_client2():
    headers = {"Origin": "www.somesite.com"}
    jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(
        cookie_jar=jar,
        headers=headers
    )

    yield session

    await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = Redis(
        host=auth_test_settings.redis_host,
        port=auth_test_settings.redis_port,
    )
    yield redis
    await redis.aclose()


@pytest_asyncio.fixture(scope='session')
async def async_engine() -> AsyncEngine:
    DSN = (
        f'postgresql+asyncpg://{auth_test_settings.auth_db_user}:{auth_test_settings.auth_db_password}'
        f'@{auth_test_settings.auth_db_host}:{auth_test_settings.auth_db_port}/{auth_test_settings.auth_db}'
    )
    return create_async_engine(DSN, echo=False, future=True)


@pytest_asyncio.fixture(scope='module')
async def prepare_database(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
async def async_connection(async_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture(scope='session')
async def async_session(async_connection: AsyncConnection):
    async with AsyncSession(bind=async_connection) as session:
        yield session


@pytest_asyncio.fixture(scope="module")
def random_creds():
    faker = Faker()
    return {"username": faker.user_name(), "password": faker.password()}
