import uuid
from pydantic import EmailStr
from schemas.base import BaseSchema


class UserReadSchema(BaseSchema):
    id: uuid.UUID
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class UserCreateSchema(BaseSchema):
    username: str
    email: EmailStr
    password: str


class UserAuthSchema(BaseSchema):
    email: EmailStr
    password: str
