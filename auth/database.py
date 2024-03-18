import asyncio
from typing import AsyncGenerator, List
import uuid

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from fastapi_users_db_sqlalchemy.generics import GUID

from config import DataBaseSettings
from models.models import OAuthAccount, User

settings = DataBaseSettings()

DATABASE_URL = f"postgresql+asyncpg://{settings.USER}:{settings.PASS}@{settings.HOST}:{settings.PORT}/{settings.NAME}"

Base: DeclarativeMeta = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)



