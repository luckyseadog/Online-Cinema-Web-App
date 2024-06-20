import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from models.entity import Base
import httpx
from main import app
from core.config import settings
import json
import os
from models.entity import RoleModel, UserModel, UserRoleModel, UserHistoryModel
from datetime import datetime


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client():
    async with httpx.AsyncClient(app=app, base_url='http://localhost:8000/api/v1/auth') as client:
        yield client


@pytest_asyncio.fixture(scope='session')
async def prepare_database():
    DSN = (
        f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}'
        f'@{settings.pg_host}:{settings.pg_port}/{settings.pg_name}'
    )
    engine = create_async_engine(DSN, echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/functionals/testdata/data/roles.json') as file:
            for item in json.load(file):
                role = RoleModel(
                    id=item['id'],
                    title=item['title'],
                    description=item['description'],
                )
                session.add(role)
            await session.flush()

        with open(f'{os.path.dirname(os.path.realpath(__file__))}/functionals/testdata/data/users.json') as file:
            data = json.load(file)
            for item in data:
                user = UserModel(
                    id=item['id'],
                    login=item['login'],
                    password=item['password'],
                    email=item['email'],
                    first_name=item['first_name'],
                    last_name=item['last_name'],
                )
                session.add(user)
                print(item['roles'])

                for role in item['roles']:
                    user_role = UserRoleModel(user_id=item['id'], role_id=role['id'])
                    session.add(user_role)
            await session.flush()

            for item in data:
                for history in item['history']:
                    user_history = UserHistoryModel(
                        user_id=item['id'],
                        occured_at=datetime.strptime(history['occured_at'], '%Y-%m-%d %H:%M:%S'),
                        action=history['action'],
                        fingreprint=history['fingerprint'],
                    )
                    session.add(user_history)
            await session.flush()
        await session.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
