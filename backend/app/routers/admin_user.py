from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserUpdate, UserOut
from ..crud import user as crud_user
from ..dependencies.auth import get_current_admin
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth import authenticate_admin_user, create_access_token
from fastapi.responses import JSONResponse

from ..schemas.audit_log import AuditLogCreate
from ..crud import audit_log as crud_audit_log
from datetime import datetime, timezone

router = APIRouter(
    prefix="/admin/user",
    tags=["AdminUser"]
)

@router.post("", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        try:
            now = datetime.now(timezone.utc)
            await crud_audit_log.create_audit_log(db, AuditLogCreate(
                user_id=user.id,
                action="/admin/user",
                model="post",
                model_id=user.username,
                details=f"Create {user_in.username}",
                timestamp=now.replace(tzinfo=None)
            ))
        except Exception as e:
            print(f"⚠️ Audit log failed: {e}")
        return await crud_user.create_user(db, user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@router.get("", response_model=list[UserOut])
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

        try:
            now = datetime.now(timezone.utc)

            # Xác định hành động nếu có thay đổi khóa
            action_detail = f"Update user"
            if user_in.is_locked is not None:
                action_detail += f" (is_locked = {user_in.is_locked})"

            await crud_audit_log.create_audit_log(db, AuditLogCreate(
                user_id=user.id,
                action=f"/admin/user/{user_id}",
                model="put",
                model_id=user.username,
                details=action_detail,
                timestamp=now.replace(tzinfo=None)
            ))
        except Exception as e:
            print(f"⚠️ Audit log failed: {e}")

        return {"msg": "Updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")


@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_admin)):
    try:
        db_user = await crud_user.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        await crud_user.delete_user(db, user_id)
        try:
            now = datetime.now(timezone.utc)
            await crud_audit_log.create_audit_log(db, AuditLogCreate(
                user_id=user.id,
                action=f"/admin/user/{user_id}",
                model="delete",
                model_id=user.username,
                details=f"Delete {user_id}",
                timestamp=now.replace(tzinfo=None)
            ))
        except Exception as e:
            print(f"⚠️ Audit log failed: {e}")
        return {"msg": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")
