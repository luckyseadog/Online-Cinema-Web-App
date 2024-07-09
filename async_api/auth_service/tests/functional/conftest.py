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


# pytest_plugins = (
#     'tests.functional.fixtures.db',
# )

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


# @pytest_asyncio.fixture(scope='session')
# async def client():
#     async with httpx.AsyncClient(transport=ASGITransport(app), base_url=settings.root_path) as client:
#         yield client

@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = Redis(host=auth_test_settings.redis_host, port=auth_test_settings.redis_port)
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


@pytest_asyncio.fixture(scope='module')
async def test_user(aiohttp_client):
    """
    Creates test_user which would be checked
    """
    user_creds = {
        "login": "john",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepassword123"
    }
    url = Path(f'{auth_test_settings.root_path}') / "signup"

    async with aiohttp_client.post(url, json=user_creds) as resp:
        resp.raise_for_status()








# @pytest_asyncio.fixture(scope='function')
# async def superadmin_cookies(prepare_database, super_admin, client):
#     response = await client.post(
#         '/login', data={
#             'username': settings.sa_login,
#             'password': settings.sa_password,
#         },
#         headers={'Origin': settings.root_path},
#     )
#     yield response.cookies


# @pytest_asyncio.fixture(scope='session')
# async def prepare_database():
#     DSN = (
#         f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_pass}'
#         f'@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}'
#     )
#     engine = create_async_engine(DSN, echo=False, future=True)
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest_asyncio.fixture(scope='session')
# async def prepare_database():
#     DSN = (
#         f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_pass}'
#         f'@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}'
#     )
#     engine = create_async_engine(DSN, echo=True, future=True)
#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session() as session:
#         with open(f'{os.path.dirname(os.path.realpath(__file__))}/functional/testdata/data/roles.json') as file:
#             for item in json.load(file):
#                 role = RoleModel(
#                     id=item['id'],
#                     title=item['title'],
#                     description=item['description'],
#                 )
#                 session.add(role)
#             await session.flush()
#
#         with open(f'{os.path.dirname(os.path.realpath(__file__))}/functional/testdata/data/users.json') as file:
#             data = json.load(file)
#             for item in data:
#                 user = UserModel(
#                     id=item['id'],
#                     login=item['login'],
#                     password=item['password'],
#                     email=item['email'],
#                     first_name=item['first_name'],
#                     last_name=item['last_name'],
#                 )
#                 session.add(user)
#                 print(item['roles'])
#
#                 for role in item['roles']:
#                     user_role = UserRoleModel(user_id=item['id'], role_id=role['id'])
#                     session.add(user_role)
#             await session.flush()
#
#             for item in data:
#                 for history in item['history']:
#                     user_history = UserHistoryModel(
#                         user_id=item['id'],
#                         occured_at=datetime.strptime(history['occured_at'], '%Y-%m-%d %H:%M:%S'),
#                         action=history['action'],
#                         fingerprint=history['fingerprint'],
#
#                     )
#                     session.add(user_history)
#             await session.flush()
#         await session.commit()
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)



# FROM folder fixtures



# @pytest_asyncio.fixture(scope='function')
# async def roles_in_db(async_session: AsyncSession):
#     with open(f'{os.path.dirname(os.path.realpath(__file__))}/../testdata/data/roles.json') as file:
#         for item in json.load(file):
#             role = RoleModel(
#                 id=item['id'],
#                 title=item['title'],
#                 description=item['description'],
#             )
#             async_session.add(role)
#         await async_session.flush()
#         await async_session.commit()


# @pytest_asyncio.fixture(scope='function')
# async def users_in_db(async_session: AsyncSession):
#     with open(f'{os.path.dirname(os.path.realpath(__file__))}/../testdata/data/users.json') as file:
#         data = json.load(file)
#         for item in data[:10]:
#             user = UserModel(
#                 id=item['id'],
#                 login=item['login'],
#                 password=password_service.compute_hash(item['password']),
#                 email=item['email'],
#                 first_name=item['first_name'],
#                 last_name=item['last_name'],
#             )
#             async_session.add(user)
#         await async_session.flush()
#         await async_session.commit()

        # data = json.load(file)
        #             for item in data:
        #                 user = UserModel(
        #                     id=item['id'],
        #                     login=item['login'],
        #                     password=password_service.compute_hash(item['password']),
        #                     email=item['email'],
        #                     first_name=item['first_name'],
        #                     last_name=item['last_name'],
        #                 )
        #                 async_session.add(user)


# @pytest_asyncio.fixture(scope='function')
# async def super_admin(async_session: AsyncSession):
#     role_id = str(uuid4())
#     user_id = str(uuid4())

#     role = RoleModel(
#         id=role_id,
#         title=settings.role_super_admin,
#         description=f'{settings.role_super_admin} description',
#     )
#     async_session.add(role)
#     await async_session.flush()

#     user = UserModel(
#         id=user_id,
#         login=settings.sa_login,
#         password=password_service.compute_hash(settings.sa_password),
#         email=settings.sa_email,
#         first_name=settings.sa_firstname,
#         last_name=settings.sa_lastname,
#     )
#     async_session.add(user)
#     await async_session.flush()

#     user_role = UserRoleModel(user_id=user_id, role_id=role_id)
#     async_session.add(user_role)
#     await async_session.commit()


# @pytest_asyncio.fixture(scope='session')
# async def fill_db(async_session: AsyncSession):
#     with open(f'{os.path.dirname(os.path.realpath(__file__))}/../testdata/data/roles.json') as file:
#         for item in json.load(file):
#             role = RoleModel(
#                 id=item['id'],
#                 title=item['title'],
#                 description=item['description'],
#             )
#             async_session.add(role)
#         await async_session.flush()
#
#         with open(f'{os.path.dirname(os.path.realpath(__file__))}/../testdata/data/users.json') as file:
#             data = json.load(file)
#             for item in data:
#                 user = UserModel(
#                     id=item['id'],
#                     login=item['login'],
#                     password=password_service.compute_hash(item['password']),
#                     email=item['email'],
#                     first_name=item['first_name'],
#                     last_name=item['last_name'],
#                 )
#                 async_session.add(user)
#
#                 for role in item['roles']:
#                     user_role = UserRoleModel(user_id=item['id'], role_id=role['id'])
#                     async_session.add(user_role)
#             await async_session.flush()
#
#             for item in data:
#                 for history in item['history']:
#                     user_history = UserHistoryModel(
#                         user_id=item['id'],
#                         occured_at=datetime.strptime(history['occured_at'], '%Y-%m-%d %H:%M:%S'),
#                         action=history['action'],
#                         fingerprint=history['fingerprint'],
#
#                     )
#                     async_session.add(user_history)
#             await async_session.flush()
#         await async_session.commit()
    # yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
