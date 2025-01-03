import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import admin, auth, roles, users
from core.logger import LOGGING
from db import postgres_db, redis_db
from src.services.token_bucket_service import get_token_bucket
from src.middleware.token_bucket_middleware import TokenBucketMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('start')
    pg_session = postgres_db.get_session()
    redis_db.redis = redis_db.get_redis()

    background_tasks = set()
    token_bucket = get_token_bucket()
    task = asyncio.create_task(token_bucket.start_fill_bucket_process())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    await pg_session.aclose()
    await redis_db.redis.close()
    logging.info('end')


app = FastAPI(
    title='Online Cinema Authorization Service',
    description='',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(TokenBucketMiddleware)

app.include_router(admin.router, prefix='/api/v1/auth/admin', tags=['admin'])
app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(users.router, prefix='/api/v1/auth', tags=['users'])
app.include_router(roles.router, prefix='/api/v1/auth/admin', tags=['roles'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
