from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.user import UserCreate, UserLogin, UserOut
from ..services.auth import create_access_token, get_password_hash, verify_password

router = APIRouter()

fake_users_db = {}

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_data = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "ten_chi_nhanh": user.ten_chi_nhanh,
        "hashed_password": hashed_password,
        "is_admin": user.is_admin
    }
    fake_users_db[user.username] = user_data
    return UserOut(**user_data)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
