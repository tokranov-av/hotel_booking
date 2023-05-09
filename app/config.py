from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения"""
    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    @property
    def database_url(self):
        user = f'{self.DB_USER}:{self.DB_PASS}'
        database = f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return f'postgresql+asyncpg://{user}@{database}'

    @property
    def test_database_url(self):
        user = f'{self.TEST_DB_USER}:{self.TEST_DB_PASS}'
        database = (
            f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )
        return f'postgresql+asyncpg://{user}@{database}'

    class Config:
        env_file = '.env'


settings = Settings()
