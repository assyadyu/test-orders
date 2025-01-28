from os import environ

from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


class Settings(BaseSettings):
    DEBUG: bool = environ.get("DEBUG", default=True)

    PG_USER: str = environ.get("POSTGRES_USER", default="")
    PG_PASSWORD: str = environ.get("POSTGRES_PASSWORD", default="")
    PG_DB: str = environ.get("POSTGRES_DB", default="")
    PG_HOST: str = environ.get("POSTGRES_HOST", default="")
    PG_PORT: str = environ.get("POSTGRES_PORT", default="")

    SECRET_KEY: str = environ.get("SECRET_KEY", default="")
    AUTH_URL: str = environ.get("AUTH_URL", default="")

    REDIS_HOST: str = environ.get("REDIS_HOST", default="")
    REDIS_PORT: str = environ.get("REDIS_PORT", default="")

    RABBITMQ_HOST: str = environ.get('RABBITMQ_HOST', default="")
    RABBITMQ_PORT: str = environ.get('RABBITMQ_PORT', default="")
    RABBITMQ_USER: str = environ.get('RABBITMQ_USER', default="guest")
    RABBITMQ_PASSWORD: str = environ.get('RABBITMQ_PASSWORD', default="guest")
    RABBITMQ_QUEUE: str = environ.get('RABBITMQ_QUEUE', default="orders")
    RABBITMQ_ROUTE: str = environ.get('RABBITMQ_ROUTE', default="orders")

    @property
    def db_url(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.PG_USER,
            self.PG_PASSWORD,
            self.PG_HOST,
            self.PG_PORT,
            self.PG_DB
        )  # noqa E501

    @property
    def rabbitmq_url(self):
        return "amqp://{}:{}@{}:{}/".format(
            self.RABBITMQ_USER,
            self.RABBITMQ_PASSWORD,
            self.RABBITMQ_HOST,
            self.RABBITMQ_PORT,
        )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
