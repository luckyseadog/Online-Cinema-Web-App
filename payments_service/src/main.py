import logging

import uvicorn
from api.v1.payment_routs import payment_router
from api.v1.redirect_routs import redirect_router
from api.v1.webhook_routs import webhook_router
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, ORJSONResponse

app = FastAPI(
    title='Online Cinema Payment Service',
    description='',
    version='1.0.0',
    docs_url='/payments/openapi',
    openapi_url='/payments/openapi.json',
    default_response_class=ORJSONResponse,
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return JSONResponse({"status": "ok"})

app.include_router(payment_router, prefix='/payments/v1', tags=['payment'])
app.include_router(redirect_router, prefix='/payments/v1', tags=['redirect'])
app.include_router(webhook_router, prefix='/payments/v1', tags=['webhook'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
    )
