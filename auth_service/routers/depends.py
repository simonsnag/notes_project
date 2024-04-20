from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.dal import UserDAL
from models.models import User

bearer_scheme = HTTPBearer(bearerFormat="JWT")


async def get_current_user(
    http_auth: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_dal: UserDAL = Depends(),
) -> User:
    token = http_auth.credentials
    user = await user_dal.get_current_user_by_jwt(token)

    return user


async def get_token(
    http_auth: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_dal: UserDAL = Depends(),
) -> dict:
    token = http_auth.credentials
    refreshed_token = await user_dal.refresh_access_token(token)
    return refreshed_token
