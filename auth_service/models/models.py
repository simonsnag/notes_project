import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)

    def verify_password(self, password) -> bool:
        correct_password = pwd_context.verify(password, self.hashed_password)
        return correct_password
