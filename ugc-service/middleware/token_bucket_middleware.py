from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from services.token_bucket_service import get_token_bucket


class TokenBucketMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self._token_bucket = get_token_bucket()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse:
        if request.scope["path"] in {"/api/openapi", "/api/openapi.json", "/api/redoc"}:
            return await call_next(request)

        if await self._token_bucket.request_permisson(request.client.host if request.client else ""):
            return await call_next(request)

        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"message": "Too many requests"})
