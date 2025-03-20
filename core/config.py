# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
model_config = SettingsConfigDict(env_nested_delimiter='__')


class Setting(BaseSettings):
    SQLALCHEMY_DATABASE_NAME: str
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = "env/.env"


settings = Setting()