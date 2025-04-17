from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, user
from .database import engine, Base
from .routers import report
from .routers import loai_baocao
from .routers import yeu_cau
from .routers import audit_log

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/admin/user", tags=["Admin User"])
app.include_router(audit_log.router, prefix="/admin", tags=["Audit Log"])
app.include_router(report.router, prefix="/report", tags=["Report"])
app.include_router(loai_baocao.router, prefix="/admin/loaibaocao", tags=["Loại báo cáo"])
app.include_router(yeu_cau.router, prefix="/report/request", tags=["Yêu cầu báo cáo"])

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/ping")
async def ping():
    return {"msg": "pong"}



