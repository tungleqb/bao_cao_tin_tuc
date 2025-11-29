from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..dependencies.auth import get_current_user
from datetime import datetime, timezone

router = APIRouter()

@router.get("/server-time")
async def get_server_time(current_user=Depends(get_current_user)):
    return {"now": datetime.now(timezone.utc).isoformat()}
