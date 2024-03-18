import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: EmailStr
    user_name: str

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    user_name: str
    email: EmailStr
    password: str


