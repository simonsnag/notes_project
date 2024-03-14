import uuid

from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from app.auth.auth import auth_backend
from app.auth.schemas import UserCreate, UserRead
from app.auth.manager import get_user_manager
from app.auth.manager import current_active_user

from app.auth.database import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
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

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}