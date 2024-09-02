from collections.abc import AsyncGenerator, Callable, Coroutine
from typing import Any

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from testdata.alchemy_model import Base


@pytest_asyncio.fixture(name="engine", scope="session")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def engine() -> AsyncEngine:
    return create_async_engine(test_settings.postgres_url, echo=True)


@pytest_asyncio.fixture(name="async_session", scope="session")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def async_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(name="session", scope="session")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def session(async_session: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="purge_database")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
async def purge_database(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(name="create_database")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def create_database(engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return inner


@pytest_asyncio.fixture(name="drop_database")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def drop_database(engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    return inner
