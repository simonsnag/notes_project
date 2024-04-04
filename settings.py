from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DataBaseSettings(BaseSettings):
    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str


class CryptoSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
