from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import access_control
from src.core.config import configs
from src.db import redis
from src.models.errors import ErrorBody
from src.services.custom_error import AlreadyExistError


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis.redis = Redis(host=configs.redis_host, port=configs.redis_port)
    yield
    await redis.redis.close()


tags_metadata = [access_control.rights_tags_metadata]

responses: dict[str | int, Any] = {status.HTTP_412_PRECONDITION_FAILED: {"model": ErrorBody}}

app = FastAPI(
    title=configs.project_name,
    description="",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    openapi_tags=tags_metadata,
    default_response_class=ORJSONResponse,
    responses=responses,
    lifespan=lifespan,
)


@app.exception_handler(AlreadyExistError)
async def edo_fatal_error_handler(request: Request, exc: AlreadyExistError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        content=exc.response.model_dump(),
    )


app.include_router(access_control.router, prefix="/auth/v1/access_control")
