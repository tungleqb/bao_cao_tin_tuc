from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..config import settings
from jose import JWTError, jwt
from ..schemas.user import UserOut
from ..database import get_db
from ..services.auth import get_user_by_username
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        db_user = await get_user_by_username(db, username)
        if db_user is None:
            raise credentials_exception
        return UserOut.model_validate(db_user)
    except JWTError:
        raise credentials_exception

async def get_current_admin(user: UserOut = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Không có quyền truy cập")
    return user
