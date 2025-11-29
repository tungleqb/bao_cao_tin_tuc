from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..database import get_db
from ..schemas.user import UserOut
from ..services.auth import decode_token
from ..crud.user import get_user
from fastapi import Request

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/user/login")

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> UserOut:
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token")
        try:
            payload = decode_token(token)
            user_id_raw = payload.get("sub")
            if user_id_raw is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            try:
                user_id = int(user_id_raw)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token `sub` must be integer")

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        db_user = await get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        print("✅ Authenticated user:", db_user.username)
        print("✅ Is admin:", db_user.is_admin)
        return UserOut.model_validate(db_user)
    except HTTPException as e:  
        print(f"❌ Error in get_current_user: {e.detail}")
        raise e
    except Exception as e:
        print(f"❌ Unexpected error in get_current_user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def get_current_admin(user: UserOut = Depends(get_current_user)):
    try:
        print(f"🧪 Kiểm tra quyền admin của user {user.username} - is_admin={user.is_admin}")
        if not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
        return user
    except HTTPException as e:
        print(f"❌ Error in get_current_admin: {e.detail}")
        raise e
    except Exception as e:
        print(f"❌ Unexpected error in get_current_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")