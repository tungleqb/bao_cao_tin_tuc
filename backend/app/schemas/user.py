from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class UserBase(BaseModel):
    username: str
    name: Optional[str] = None
    level: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    level: Optional[str] = None
    is_admin: bool
    time_created: Optional[datetime] = None  # ✅ Bổ sung
    avatar: Optional[str] = None              # ✅ Bổ sung

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str