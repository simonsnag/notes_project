from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from db.database import get_async_session
from models.models import UserDB, pwd_context
from schemas.user import UserAuthSchema, UserCreateSchema
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Response

from settings import AdminSettings, CryptoSettings


class UserDAL():
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user: UserCreateSchema):
            hashed_password = pwd_context.hash(user.password)
            new_user = UserDB(
                username = user.username,
                email = user.email,
                hashed_password = hashed_password
                )
            
            status_email = await self.check_email(self.db_session, new_user.email)
            
            if status_email:
                raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует.")
            
            self.db_session.add(new_user)
            await self.db_session.commit()
            
            return f"Пользователь удачно зарегистрирован!"
        
    async def auth_user(self, response: Response, useremail: str, userpassword: str):
        query = select(UserDB).where(UserDB.email == useremail)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                            status_code=401,
                            detail="Такого пользователя не существует"
                        )
        
        correct_password = user.verify_password(userpassword)
        if not correct_password:
            raise HTTPException(status_code=401, detail="Неправильный пароль")
            
        access_token = await self.create_refresh_token(data={"sub": useremail}, expires_delta=timedelta(minutes=30))
        response.set_cookie(key="access_token", value=f"{access_token}")
        return {"access_token": access_token, "token_type": "bearer"}
            

    async def get_current_user_by_jwt(self, token: str):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Данный пользователь не прошел авторизацию.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if token is None:
             raise credentials_exception

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            useremail = payload.get("sub")
            if useremail is None:
                raise credentials_exception
            token_data = {"useremail": useremail}
        except JWTError:
            raise credentials_exception
        
        query = select(UserDB).filter(UserDB.email == token_data["useremail"])
        result = await self.db_session.execute(query)
        current_user = result.scalars().first()
        
        if current_user is None:
            raise credentials_exception
        
        return current_user.email
    
    async def refresh_access_token(self, response: Response, refresh_token: str):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if refresh_token is None:
            raise credentials_exception
        try:
            payload = jwt.decode(refresh_token, "secret", algorithms=["HS256"])
            
            useremail = payload.get("sub")
            if useremail is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception
        
        access_token = await self.create_refresh_token(
            data={"sub": useremail}, expires_delta=timedelta(hours=24)
        )

        response.set_cookie(key="access_token", value=f"{access_token}")
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    
    async def check_email(self, session, email_to_check: str):
        query = select(UserDB).where(UserDB.email == email_to_check)
        result = await session.execute(query)
        email_exists = result.scalar() is not None
        return email_exists

    
    async def create_refresh_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
        return encoded_jwt
    
