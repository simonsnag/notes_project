from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal import UserDAL
from schemas.user import UserAuthSchema, UserCreateSchema
from tests.conftest import api_client


pytestmark = [pytest.mark.anyio]


async def test_create_user(api_client, db: AsyncSession):
    user_create = {
        "username": "sam",
        "email": "sam@example.com",
        "password": "sam"
    }
    
    response = await api_client.post("/user/create", json=user_create)
    assert response.status_code == 200 
    assert response.json() == "Пользователь удачно зарегистрирован!"
    
    user_create = {
        "username": "sammy",
        "email": "sam@example.com",
        "password": "sam"
    }

    response = await api_client.post("/user/create", json=user_create)
    assert response.status_code == 409
    assert response.json() == {"detail": "Пользователь с таким email уже существует."}

async def test_auth_user(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(username="sam", email="sam@example.com", password="sam")
    await user_dal.create_user(user_create)
    user_auth = {
        "email": "sam@example.com",
        "password": "sam"
    }

    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    user_auth = {
        "email": "sammym@example.com",
        "password": "sam"
    }

    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 401
    assert response.json()["detail"] == "Такого пользователя не существует"

    user_auth = {
        "email": "sam@example.com",
        "password": "sammmy"
    }
    
    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 401
    assert response.json()["detail"] == "Неправильный пароль"


async def test_get_user_by_jwt(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(username="sam", email="sam@example.com", password="sam")
    await user_dal.create_user(user_create)

    user_auth = {
        "email": "sam@example.com",
        "password": "sam"
    }

    await api_client.post("/user/auth", json=user_auth)

    response = await api_client.get("/user/auth")
    assert response.status_code == 200
    assert response.json() == user_auth["email"]

    api_client.cookies.clear()
    
    response = await api_client.get("/user/auth")
    assert response.status_code == 401
    assert response.json()["detail"] == "Данный пользователь не прошел авторизацию."


async def test_create_refresh_token(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(username="sam", email="sam@example.com", password="sam")
    await user_dal.create_user(user_create)

    user_auth = {
        "email": "sam@example.com",
        "password": "sam"
    }

    old_token = await api_client.post("/user/auth", json=user_auth)
    old_token = old_token.json()["access_token"]

    response = await api_client.post("/user/token/refresh")
    assert response.status_code == 200
    assert response.json()["access_token"] != old_token

    api_client.cookies.clear()

    response = await api_client.post("/user/token/refresh")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"











