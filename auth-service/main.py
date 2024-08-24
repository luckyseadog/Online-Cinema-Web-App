from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse, JSONResponse
from redis.asyncio import Redis

from api.v1 import films, genres
from core.config import configs
from api.v1 import persons
from db import redis
from services.errors import ContentError


tags_metadata = [
    films.films_tags_metadata,
    genres.genres_tags_metadata,
    persons.persons_tags_metadata,
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis.redis = Redis(host=configs.redis_host, port=configs.redis_port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=configs.project_name,
    description="",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    redoc_url="/api/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# @app.exception_handler(ContentError)
# async def edo_fatal_error_handler(request: Request, exc: ContentError) -> JSONResponse:
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content={"message": exc.message},
#     )


# app.include_router(films.router, prefix="/api/v1/films")
# app.include_router(genres.router, prefix="/api/v1/genres")
# app.include_router(persons.router, prefix="/api/v1/persons")
