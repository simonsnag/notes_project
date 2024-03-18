import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class DataBaseSettings(BaseSettings):
    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASS: str
    class Config():
        env_prefix = "db_"



class AdminSettings(BaseSettings):
    AUTH_PASS: str
    MANAGER_PASS: str   
    class Config():
        env_prefix = ""