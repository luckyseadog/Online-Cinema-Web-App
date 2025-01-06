import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any, NoReturn

import sentry_sdk
from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from beanie import init_beanie
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse, ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import get_tracer
from opentelemetry.trace.propagation import get_current_span
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.v1 import favourites, ratings, reviews
from core.config import JWTConfig, configs, jwt_config
from core.jaeger_configure import configure_tracer
from db.models import Favourite, Rating, Review
from jwt_auth_helpers import get_jwt_user_global
from middleware.token_bucket_middleware import TokenBucketMiddleware
from services import redis_service
from services.token_bucket_service import get_token_bucket


@AuthJWT.load_config
def get_config() -> JWTConfig:
    return jwt_config


tags_metadata = [
    favourites.favourites_tags_metadata,
    ratings.ratings_tags_metadata,
    reviews.reviews_tags_metadata,
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(configs.mongo_host, configs.mongo_port)
    await init_beanie(database=getattr(client, configs.mongo_name), document_models=[Rating, Review, Favourite])

    background_tasks: set[asyncio.Task[NoReturn]] = set()
    token_bucket = get_token_bucket()
    task = asyncio.create_task(token_bucket.start_fill_bucket_process())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    client.close()
    task.cancel()
    await redis_service.redis.close()


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
        ],
    )


app = FastAPI(
    title=configs.project_name,
    description="Информация по пользовательскому контенту",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    redoc_url="/api/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/sentry-debug")
async def trigger_error() -> None:
    _ = 1 / 0


app.add_middleware(TokenBucketMiddleware)  # pyright: ignore[reportCallIssue, reportArgumentType]


if configs.jaeger_on:
    FastAPIInstrumentor.instrument_app(app)

    configure_tracer()

    tracer = get_tracer(app.title)

    @app.middleware("http")
    @tracer.start_as_current_span(app.title)
    async def before_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get("X-Request-Id")
        if request_id is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "X-Request-Id is required"})

        response = await call_next(request)
        get_current_span().set_attribute("http.request_id", request_id)
        logger.info(f"{request_id}: {request.method} {request.url} {response.status_code}")
        return response


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(favourites.router, prefix="/api/v1/favourites", dependencies=[Depends(get_jwt_user_global)])
app.include_router(ratings.router, prefix="/api/v1/ratings", dependencies=[Depends(get_jwt_user_global)])
app.include_router(reviews.router, prefix="/api/v1/reviews", dependencies=[Depends(get_jwt_user_global)])
