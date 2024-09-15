from typing import Any, Coroutine

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from services.token_bucket_service import get_token_bucket
from fastapi import status
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)


class TokenBucketMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._token_bucket = get_token_bucket()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Coroutine[Any, Any, Response]:
        if request.scope["path"] in ["/api/openapi", "/api/openapi.json", "/api/redoc"]:
            return await call_next(request)

        if await self._token_bucket.request_permisson(request.client.host):
            response = await call_next(request)
            return response
        else:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"message": "Too many requests"}
            )
