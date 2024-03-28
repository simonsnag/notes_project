from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from db.database import get_async_session
from routers.users import user_router

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])

app.include_router(main_api_router)


