from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserUpdate, UserOut
from ..crud import user as crud_user
from ..dependencies.auth import get_current_admin
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth import authenticate_admin_user, create_access_token

router = APIRouter(
    prefix="/admin/user",
    tags=["AdminUser"]
)

@router.post("/login")
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_admin_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token({"sub": str(user.id), "role": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        return await crud_user.create_user(db, user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@router.get("/", response_model=list[UserOut])
async def read_users(db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        return await crud_user.get_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.put("/{user_id}")
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        db_user = await crud_user.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        await crud_user.update_user(db, user_id, user_in)
        return {"msg": "Updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")

@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await crud_user.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        await crud_user.delete_user(db, user_id)
        return {"msg": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")
