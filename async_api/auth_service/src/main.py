from fastapi import FastAPI

app = FastAPI()


@app.get("/auth")
async def root():
    return {"message": "Hello World"}