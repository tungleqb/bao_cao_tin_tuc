from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin_reporttype, admin_audit_log, admin_period, admin_report, admin_user, period, report, auth, utils
from .scheduler import start_scheduler
from contextlib import asynccontextmanager
import os
cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "")
origin_list = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield  # nơi để cleanup nếu cần
    # Ví dụ: stop_scheduler()

app = FastAPI(lifespan=lifespan)
#app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_period.router)
app.include_router(admin_user.router)
app.include_router(admin_reporttype.router)
app.include_router(admin_audit_log.router)
app.include_router(admin_report.router)
app.include_router(period.router)
app.include_router(report.router)
app.include_router(auth.router)
app.include_router(utils.router)
