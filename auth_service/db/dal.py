from datetime import datetime, timedelta

from jose import JWTError, jwt
from db.database import cryptosettings, get_async_session
from models.models import User, pwd_context
from schemas.user import UserCreateSchema
from sqlalchemy import select
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAL:
    def __init__(self, db_session: AsyncSession = Depends(get_async_session)):
        self.db_session = db_session

    async def create_user(self, user: UserCreateSchema) -> User:
        if len(user.password) < 6:
            raise HTTPException(
                status_code=401, detail="Пароль должен содержать минимум 6 символов."
            )

        hashed_password = pwd_context.hash(user.password)

        status_email = await self.check_email(user.email)

        if status_email:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email уже существует."
            )

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
        )

        self.db_session.add(new_user)
        await self.db_session.commit()

        return new_user

    async def auth_user(self, useremail: str, userpassword: str) -> dict:
        query = select(User).where(User.email == useremail)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователя с таким email не существует."
            )

        correct_password = user.verify_password(userpassword)
        if not correct_password:
            raise HTTPException(status_code=401, detail="Неправильный пароль.")

        access_token = await self.create_refresh_token(
            data={"sub": useremail}, expires_delta=timedelta(minutes=30)
        )

        return {"Authorization": f"Bearer {access_token}"}

    async def get_current_user_by_jwt(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Данный пользователь не прошел авторизацию.",
        )
        if token is None:
            raise credentials_exception

        try:
            payload = jwt.decode(
                token, cryptosettings.SECRET_KEY, algorithms=[cryptosettings.ALGORITHM]
            )
            useremail = payload.get("sub")
            if useremail is None:
                raise credentials_exception
            token_data = {"useremail": useremail}
        except JWTError:
            raise credentials_exception

        query = select(User).filter(User.email == token_data["useremail"])
        result = await self.db_session.execute(query)
        current_user = result.scalars().first()

        if current_user is None:
            raise credentials_exception

        return current_user

    async def refresh_access_token(self, refresh_token: str) -> dict:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Не подходящие данные для авторизации.",
        )

        if refresh_token is None:
            raise credentials_exception
        try:
            payload = jwt.decode(
                refresh_token,
                cryptosettings.SECRET_KEY,
                algorithms=[cryptosettings.ALGORITHM],
            )

            useremail = payload.get("sub")
            if useremail is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        access_token = await self.create_refresh_token(
            data={"sub": useremail}, expires_delta=timedelta(hours=24)
        )

        return {"Authorization": f"Bearer {access_token}"}

    async def check_email(self, email_to_check: str) -> bool:
        query = select(User).where(User.email == email_to_check)
        result = await self.db_session.execute(query)
        email_exists = result.scalar() is not None
        return email_exists

    async def create_refresh_token(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, cryptosettings.SECRET_KEY, algorithm=cryptosettings.ALGORITHM
        )
        return encoded_jwt
