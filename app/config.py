from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def database_url(self):
        user = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        database = (
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}'
        )
        return f'postgresql+asyncpg://{user}@{database}'

    class Config:
        env_file = '.env'


settings = Settings()
