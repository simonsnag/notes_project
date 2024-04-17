from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from settings import CryptoSettings, DataBaseSettings


db_settings = DataBaseSettings()
cryptosettings = CryptoSettings()

DATABASE_URL = f"postgresql+asyncpg://{db_settings.db_user}:{db_settings.db_pass}@{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
