from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str = "User"
    last_name: str = "User"
    role: str
    shift_status: str = "Clocked Out"
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    shift_status: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="user_id",
        serialization_alias="id",
    )
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    shift_status: str
    is_active: bool
    created_at: datetime