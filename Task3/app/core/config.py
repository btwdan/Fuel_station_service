import os
from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    DATABASE_URL: PostgresDsn = None
    DATABASE_TEST_URL: PostgresDsn = None

    REDIS_URL: RedisDsn

    CELERY_BROKER_URL: str = None
    CELERY_RESULT_BACKEND: str = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASS"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    @validator("DATABASE_TEST_URL", pre=True)
    def assemble_test_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER_TEST"),
            password=values.get("DB_PASS_TEST"),
            host=values.get("DB_HOST_TEST"),
            port=values.get("DB_PORT_TEST"),
            path=f"/{values.get('DB_NAME_TEST') or ''}",
        )

    @validator("CELERY_BROKER_URL", pre=True, always=True)
    def set_celery_broker(cls, v, values):
        return values.get("REDIS_URL")

    @validator("CELERY_RESULT_BACKEND", pre=True, always=True)
    def set_celery_backend(cls, v, values):
        return values.get("REDIS_URL")

    class Config:
        env_file = ".env"


settings = Settings()
