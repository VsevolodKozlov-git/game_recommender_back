from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=250)

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, max_length=250)

class UserRead(UserBase):
    id_user: int

    class Config:
        orm_mode = True