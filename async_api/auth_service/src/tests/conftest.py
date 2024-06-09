import asyncio
import json
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from models.entity import Base
from httpx import AsyncClient


# DATABASE_URL_TEST = f'postgresql+asyncpg:{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
DSN = f'postgresql+asyncpg://app:123qwe@127.0.0.1:5432/auth_test'
engine_test = create_async_engine(DSN, echo=True, future=True)
async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def create_database() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    await create_database()
    yield
    await purge_database()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()



@pytest_asyncio.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

