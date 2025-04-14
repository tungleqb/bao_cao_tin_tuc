from fastapi import FastAPI
from .routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
