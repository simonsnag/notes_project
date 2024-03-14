from typing import Optional
import uuid
from fastapi_users import models, schemas
from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column
from app.auth.database import User


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: models.ID
    user_name: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    class Config:
        from_attributes = True



class UserCreate(schemas.BaseUserCreate):
    user_name: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False

