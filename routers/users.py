from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.dal import UserDAL
from db.database import get_async_session
from models.models import UserDB
from schemas.user import UserAuthSchema, UserCreateSchema, UserDeleteSchema
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth", auto_error=False)

@user_router.post("/create")
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    new_user = UserDAL(session)
    status_of_creating = await new_user.create_user(user)
    return status_of_creating
    

@user_router.post("/auth")
async def auth_user(response: Response, user: UserAuthSchema, session: AsyncSession = Depends(get_async_session)):
    current_user = UserDAL(session)
    statuts_of_authentication = await current_user.auth_user(response, user.email, user.password)
    return statuts_of_authentication


@user_router.get("/auth")
async def read_user_me(request: Request, session: AsyncSession = Depends(get_async_session)):
    current_user = UserDAL(session)
    token = request.cookies.get("access_token")
    status_of_authorisation = await current_user.get_current_user_by_jwt(token)
    return status_of_authorisation
    

@user_router.post("/token/refresh")
async def refresh_token(response: Response, request:Request, session: AsyncSession = Depends(get_async_session)):
    current_user = UserDAL(session)
    refresh_token = request.cookies.get("access_token")
    status_of_refreshing = await current_user.refresh_access_token(response, refresh_token)
    return status_of_refreshing




        
        

