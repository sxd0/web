from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str

    LANGUAGE_CODE: ClassVar[str] = 'ru' # Возможно все сломает!

    model_config = ConfigDict(env_file=".env")

    @model_validator(mode='before')
    def validate_environment(cls, values):
        return values

settings = Settings()

