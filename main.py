import uuid
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from auth.manager import google_oauth_client

from auth.auth import SECRET, auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="notes"
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)

@app.get("/auth-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


