import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from main import app
from settings import mongo_settings
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
async def test_db():
    client = AsyncIOMotorClient(mongo_settings.database_url)
    db = client[mongo_settings.mongo_name]
    yield db
    await client.drop_database(mongo_settings.mongo_name)
