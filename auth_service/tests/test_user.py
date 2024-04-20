import pytest

from db.dal import UserDAL
from schemas.user import UserCreateSchema


pytestmark = [pytest.mark.anyio]


async def test_create_user(api_client):
    user_create = {
        "username": "samson",
        "email": "samson@example.com",
        "password": "samson",
    }

    response = await api_client.post("/user/create", json=user_create)
    assert response.status_code == 200
    assert response.json()["email"] == user_create["email"]
    assert response.json()["username"] == user_create["username"]

    user_create = {
        "username": "samson2",
        "email": "samson@example.com",
        "password": "samson2",
    }

    response = await api_client.post("/user/create", json=user_create)
    assert response.status_code == 401
    assert response.json()["detail"] == "Пользователь с таким email уже существует."

    user_create = {
        "username": "samson",
        "email": "samson@example.com",
        "password": "sam",
    }

    response = await api_client.post("/user/create", json=user_create)
    assert response.status_code == 401
    assert response.json()["detail"] == "Пароль должен содержать минимум 6 символов."


async def test_auth_user(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(
        username="sam", email="sam@example.com", password="samsam"
    )
    await user_dal.create_user(user_create)
    user_auth = {"email": "sam@example.com", "password": "samsam"}

    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 200
    assert response.json()["Authorization"][:6] == "Bearer"

    user_auth = {"email": "sammym@example.com", "password": "samsam"}

    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 401
    assert response.json()["detail"] == "Пользователя с таким email не существует."

    user_auth = {
        "email": "sam@example.com",
        "password": "sammmy",
    }

    response = await api_client.post("/user/auth", json=user_auth)
    assert response.status_code == 401
    assert response.json()["detail"] == "Неправильный пароль."


async def test_get_user_by_jwt(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(
        username="sam", email="sam@example.com", password="samsam"
    )
    await user_dal.create_user(user_create)

    user_auth = {"email": "sam@example.com", "password": "samsam"}

    response = await api_client.post("/user/auth", json=user_auth)
    headers = response.json()

    response = await api_client.get("/user/auth", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == user_auth["email"]

    user_dal = UserDAL(db)
    user_create = UserCreateSchema(
        username="sandy", email="sandy@example.com", password="sandyy"
    )
    await user_dal.create_user(user_create)

    user_auth = {"email": "sandy@example.com", "password": "sandyy"}

    response = await api_client.post("/user/auth", json=user_auth)
    headers = {"Authorization": response.json()["Authorization"] + "q"}

    response = await api_client.get("/user/auth", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Данный пользователь не прошел авторизацию."


async def test_create_refresh_token(api_client, db):
    user_dal = UserDAL(db)
    user_create = UserCreateSchema(
        username="sam", email="sam@example.com", password="samsam"
    )
    await user_dal.create_user(user_create)

    user_auth = {"email": "sam@example.com", "password": "samsam"}

    response = await api_client.post("/user/auth", json=user_auth)
    old_token = response.json()["Authorization"][7:]

    response = await api_client.post("/user/token/refresh", headers=response.json())
    assert response.status_code == 200
    assert len(response.json()["Authorization"][7:]) == len(old_token)
    assert response.json()["Authorization"][7:] != old_token

    user_dal = UserDAL(db)
    user_create = UserCreateSchema(
        username="sandy", email="sandy@example.com", password="sandyy"
    )
    await user_dal.create_user(user_create)

    user_auth = {"email": "sandy@example.com", "password": "sandyy"}

    response = await api_client.post("/user/auth", json=user_auth)
    headers = {"Authorization": response.json()["Authorization"] + "q"}

    response = await api_client.post("/user/token/refresh", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Не подходящие данные для авторизации."
