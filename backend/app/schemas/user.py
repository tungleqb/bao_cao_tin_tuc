from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    ten_chi_nhanh: str = ""
    is_admin: bool = False

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    ten_chi_nhanh: str
    is_admin: bool

    class Config:
        orm_mode = True
