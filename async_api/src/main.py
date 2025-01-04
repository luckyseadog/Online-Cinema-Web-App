import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{settings.elastic_host}:{settings.elastic_port}'])
    yield
    await redis.redis.close()
    await elastic.es.close()

app = FastAPI(
    title='Read-only API для онлайн-кинотеатра',
    description='Информация о фильмах, жанрах и людях, участвующих в создании произведений',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
