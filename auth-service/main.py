from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import access_control
from src.core.config import configs
from src.db import redis


# tags_metadata = [
#     films.films_tags_metadata,
#     genres.genres_tags_metadata,
#     persons.persons_tags_metadata,
# ]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis.redis = Redis(host=configs.redis_host, port=configs.redis_port)
    yield
    await redis.redis.close()


responses: dict[str | int, Any] = {status.HTTP_412_PRECONDITION_FAILED: {}}

app = FastAPI(
    title=configs.project_name,
    description="",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    # openapi_tags=tags_metadata,
    default_response_class=ORJSONResponse,
    responses=responses,
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
app.include_router(access_control.router, prefix="/auth/v1/access_control")
