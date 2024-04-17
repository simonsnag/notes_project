from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class PostgresSettings(BaseSettings):
    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str


postgres_settings = PostgresSettings()


class MongoSettings(BaseSettings):
    @property
    def database_url(self):
        return f"mongodb://{self.mongo_host}:{self.mongo_port}/{self.mongo_name}"

    mongo_host: str
    mongo_port: str
    mongo_name: str


mongo_settings = MongoSettings()
