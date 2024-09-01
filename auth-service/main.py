from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from redis.asyncio import Redis

from api.v1 import access_control, auth
from core.config import configs
from db import redis
from models.errors import ErrorBody
from services.custom_error import ResponseError


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis.redis = Redis(host=configs.redis_host, port=configs.redis_port)
    yield
    await redis.redis.close()


tags_metadata = [
    auth.auth_tags_metadata,
    access_control.rights_tags_metadata
]

responses: dict[str | int, Any] = {
    status.HTTP_421_MISDIRECTED_REQUEST: {"model": ErrorBody},
}


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


@app.exception_handler(ResponseError)
async def misdirected_error_handler(request: Request, exc: ResponseError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_421_MISDIRECTED_REQUEST,
        content=exc.response.model_dump(),
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(auth.router, prefix="/auth/v1/auth")
app.include_router(access_control.router, prefix="/auth/v1/access_control")
