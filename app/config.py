from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

database_settings = DatabaseSettings()

DATABASE_URL = (
    f"postgresql+asyncpg://{database_settings.POSTGRES_USER}:"
    f"{database_settings.POSTGRES_PASSWORD}@{database_settings.POSTGRES_SERVER}:"
    f"{database_settings.POSTGRES_PORT}/{database_settings.POSTGRES_DB}"
)