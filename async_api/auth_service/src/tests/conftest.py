import asyncio
import json
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
import pytest_asyncio
from models.entity import Base
import httpx
from main import app

from models import User, Role
from schemas import UserCreate
from fastapi import Depends
from faker import Faker

# DATABASE_URL_TEST = f'postgresql+asyncpg:{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
DSN = f'postgresql+asyncpg://app:123qwe@127.0.0.1:5432/auth_test'
engine_test = create_async_engine(DSN, echo=True, future=True)
async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


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



# @pytest_asyncio.fixture(scope='session')
# async def client():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client



@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client

async def create_users(db: AsyncSession = Depends(get_session)):
    faker = Faker()
    Users = []

    res = db.scalars(
            insert(Users).values(
            [
                {
                    "login": faker.user_name(),
                    "password": faker.password(),
                    "first_name": faker.first_name(),
                    "last_name": faker.last_name(),
                    "email": faker.email()
                } for _ in range(10)],
            )
        )
    await dbmmit()
    await db.refresh(user)


