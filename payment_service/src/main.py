import logging

import uvicorn
from api.v1.payments_router import router
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, ORJSONResponse

app = FastAPI(
    title='Online Cinema Payment Service',
    description='',
    version='1.0.0',
    docs_url='/pay/openapi',
    openapi_url='/pay/openapi.json',
    default_response_class=ORJSONResponse,
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return JSONResponse({"status": "ok"})

app.include_router(router, prefix='/pay/v1', tags=['payment'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
    )
