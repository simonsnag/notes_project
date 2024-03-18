from typing import List
import uuid
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID
from pydantic import EmailStr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData


class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] =  mapped_column(nullable=False)
    user_name: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool]
    is_active: Mapped[bool]
    is_verified: Mapped[bool]
    oauthaccounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )





