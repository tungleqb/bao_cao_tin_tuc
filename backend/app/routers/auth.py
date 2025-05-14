from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services import auth as auth_service
from ..schemas.user import Token
from ..schemas.user import UserCreate, UserUpdate, UserOut, PasswordChange
from ..dependencies.auth import get_current_user
from ..services.auth import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        token = auth_service.create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.get("/me", response_model=UserOut)
async def get_current_user_info(user: UserOut = Depends(get_current_user)):
    return user

@router.post("/changepassword", status_code=200)
async def change_password(
    payload: PasswordChange,
    db: AsyncSession = Depends(get_db),
    user: UserOut = Depends(get_current_user)):
    try:
        from ..crud.user import get_user, update_password_only

        db_user = await get_user(db, user.id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # ✅ Kiểm tra mật khẩu cũ có đúng không
        hashed_password = db_user.hashed_password
        if not verify_password(payload.old_password, hashed_password):
            raise HTTPException(status_code=401, detail="Mật khẩu cũ không đúng")

        await update_password_only(db, user.id, payload.new_password)
        return {"message": "Đổi mật khẩu thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during password change: {str(e)}")
