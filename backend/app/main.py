from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin_user, admin_report_type, period, report, auth, admin_audit_log
from fastapi.openapi.utils import get_openapi
from .scheduler import start_scheduler
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield  # nơi để cleanup nếu cần
    # Ví dụ: stop_scheduler()

app = FastAPI(lifespan=lifespan)
#app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_user.router)
app.include_router(admin_report_type.router)
app.include_router(admin_audit_log.router)
app.include_router(period.router)
app.include_router(report.router)
app.include_router(auth.router)


# ✅ Custom OpenAPI để Swagger gửi token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Report System API",
        version="1.0.0",
        description="API backend hệ thống báo cáo.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if isinstance(method, dict):  # bảo vệ chống lỗi
                method["security"] = [{"BearerAuth": []}]  # ✅ Bắt buộc thêm security
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
