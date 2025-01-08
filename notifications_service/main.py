import asyncio
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sentry_sdk import capture_exception
from src.api.v1.router import router
from src.db.redis_db import get_redis
from src.services.rate_limiter_service import get_token_bucket
from starlette.responses import JSONResponse

sentry_sdk.init(
    dsn="https://31f851ef6701ed81a40491df6b831fbd@o4508461491552256.ingest.de.sentry.io/4508461493911632",
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_service = get_redis()

    background_tasks = set()
    token_bucket = get_token_bucket()
    task = asyncio.create_task(token_bucket.start_fill_bucket_process())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    task.cancel()
    await redis_service.aclose()


app = FastAPI(
    version="1.0.0",
    docs_url='/notifications/openapi',
    openapi_url='/notifications/openapi.json',
    lifespan=lifespan,
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    capture_exception(exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

app.include_router(router, prefix='/notifications/v1', tags=['notifications'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
