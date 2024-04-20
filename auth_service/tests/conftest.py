import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from db.database import get_async_session
from main import app
from models.models import Base
from settings import DataBaseSettings

settings = DataBaseSettings()


@pytest.fixture
def test_db_name():
    test_db_name = f"{uuid.uuid4().hex}_pytest"
    return test_db_name


async def create_database(test_db_name):
    url = make_url(settings.database_url)
    url = url.set(database="postgres")
    template_engine = create_async_engine(url, echo=False)

    async with template_engine.begin() as conn:
        await conn.execute(text("ROLLBACK"))
        await conn.execute(text(f'CREATE DATABASE "{test_db_name}";'))
        await conn.commit()
        await conn.close()
        await template_engine.dispose()


@pytest.fixture
async def sa_engine_db_async(test_db_name):
    await create_database(test_db_name)

    url = make_url(settings.database_url)
    url = url.set(database=test_db_name)
    a_engine = create_async_engine(
        url, poolclass=NullPool, connect_args={"server_settings": {"jit": "off"}}
    )

    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield a_engine
    finally:
        async with a_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await a_engine.dispose()


@pytest.fixture
async def db(sa_engine_db_async):
    async_session = async_sessionmaker(
        sa_engine_db_async,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def patch_sessionmaker(db, monkeypatch) -> None:
    app.dependency_overrides[get_async_session] = lambda: db

    async def call(*args, **kwargs) -> AsyncSession:
        """Патч вызова sessionmaker.__call__(), который происходит в async_session(), in_transaction"""
        return await db

    monkeypatch.setattr(sessionmaker, "__call__", call)


@pytest.fixture
async def api_client(patch_sessionmaker) -> AsyncClient:
    async with AsyncClient(app=app, base_url="https://test") as async_client:
        yield async_client


@pytest.fixture
def anyio_backend():
    return "asyncio"
