from fastapi import FastAPI
from .routers import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# 👇 Thêm đoạn này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
