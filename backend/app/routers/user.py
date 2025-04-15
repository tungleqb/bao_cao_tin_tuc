from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserOut
from ..models.user import User
from ..services.auth import get_user_by_username, get_password_hash
from ..database import get_db
from ..dependencies.auth import get_current_admin
from sqlalchemy.future import select

router = APIRouter()

@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    if await get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        ten_chi_nhanh=user.ten_chi_nhanh,
        is_admin=user.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    db_user.username = user.username
    db_user.hashed_password = get_password_hash(user.password)
    db_user.ten_chi_nhanh = user.ten_chi_nhanh
    db_user.is_admin = user.is_admin
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    await db.delete(db_user)
    await db.commit()
    return {"msg": "Đã xoá tài khoản thành công"}
