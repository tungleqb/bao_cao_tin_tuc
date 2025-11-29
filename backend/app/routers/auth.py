from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.auth import authenticate_admin_user, create_access_token, authenticate_user
from ..schemas.user import Token
from ..schemas.user import UserCreate, UserUpdate, UserOut, PasswordChange
from ..dependencies.auth import get_current_user
from ..services.auth import verify_password
from ..crud.user import get_user, update_password_only
from fastapi.responses import JSONResponse
from ..schemas.audit_log import AuditLogCreate
from ..crud import audit_log as crud_audit_log
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/admin")
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_admin_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if user.is_locked:
        raise HTTPException(status_code=403, detail="Tài khoản quản trị đã bị khóa.")
    access_token = create_access_token({"sub": str(user.id), "isAdmin": "true"})
    response = JSONResponse(content={"message": "Login success"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",  # hoặc "Lax"
        max_age=3600,
        path="/")
    try:
        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action="/auth/admin",
            model="post",
            model_id=user.username,
            details=f"Logined {user.username}",
            timestamp=now.replace(tzinfo=None)
        ))
    except Exception as e:
        print(f"⚠️ Audit log failed: {e}")
    return response

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if user.is_locked:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên.")
    access_token = create_access_token({"sub": str(user.id), "isAdmin": "false"})
    response = JSONResponse(content={"message": "Login success"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",  # hoặc "Lax"
        max_age=3600,
        path="/"
    )
    try:
        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action="/auth/login",
            model="post",
            model_id=user.username,
            details=f"Logined {user.username}",
            timestamp=now.replace(tzinfo=None)
        ))
    except Exception as e:
        print(f"⚠️ Audit log failed: {e}")
    return response

@router.post("/logout")
async def logout(user: UserOut = Depends(get_current_user)):
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response

@router.get("/me", response_model=UserOut)
async def get_current_user_info(user: UserOut = Depends(get_current_user)):
    return user

@router.post("/changepassword", status_code=200)
async def change_password(
    payload: PasswordChange,
    db: AsyncSession = Depends(get_db),
    user: UserOut = Depends(get_current_user)):
    db_user = await get_user(db, user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Kiểm tra mật khẩu cũ có đúng không
    hashed_password = db_user.hashed_password
    if not verify_password(payload.old_password, hashed_password):
        raise HTTPException(status_code=401, detail="Mật khẩu cũ không đúng")

    await update_password_only(db, user.id, payload.new_password)
    try:
        now = datetime.now(timezone.utc)
        await crud_audit_log.create_audit_log(db, AuditLogCreate(
            user_id=user.id,
            action="/auth/changepassword",
            model="post",
            model_id=user.username,
            details=f"Logined {user.username}",
            timestamp=now.replace(tzinfo=None)
        ))
    except Exception as e:
        print(f"⚠️ Audit log failed: {e}")
    return {"message": "Đổi mật khẩu thành công"}
