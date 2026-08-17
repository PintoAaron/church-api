from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    AUTH_SECRETE_KEY: str
    AUTH_ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_NAME: Optional[str] = None
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool | None = True
    MAIL_SSL_TLS: bool | None = False
    MAIL_USE_CREDENTIALS: bool | None = True
    MAIL_VALIDATE_CERTS: bool | None = True
    REDIS_URL: str | None = "localhost"
    REDIS_PORT: int | None = "6379"
    ADMIN_DEFAULT_USERNAME: str
    ADMIN_DEFAULT_EMAIL: EmailStr
    ADMIN_DEFAULT_PASSWORD: str
    ADMIN_DEFAULT_ROLE: str


envConfig = EnvConfig()
