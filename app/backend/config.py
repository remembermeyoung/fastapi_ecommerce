from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# load_dotenv('app/backend/.env')


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file="app/backend/.env", env_file_encoding="utf-8")


settings = Settings()
