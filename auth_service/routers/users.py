from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from db.dal import UserDAL
from db.database import get_async_session
from models.models import User
from routers.depends import get_current_user, get_token
from schemas.user import UserAuthSchema, UserCreateSchema, UserReadSchema
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth", auto_error=False)


@user_router.post("/create", response_model=UserReadSchema)
async def create_user(
    user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)
) -> UserReadSchema:
    new_user = UserDAL(session)
    user_read = await new_user.create_user(user)
    return UserReadSchema.model_validate(user_read)


@user_router.post("/auth", response_model=dict)
async def auth_user(
    user: UserAuthSchema, session: AsyncSession = Depends(get_async_session)
) -> dict:
    current_user = UserDAL(session)
    jwt_token = await current_user.auth_user(user.email, user.password)
    return jwt_token


@user_router.get("/auth", response_model=UserReadSchema)
async def get_user(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> UserReadSchema:
    return UserReadSchema.model_validate(user)


@user_router.post("/token/refresh", response_model=dict)
async def refresh_token(
    token: str = Depends(get_token),
    session: AsyncSession = Depends(get_async_session),
) -> str:
    return token
