
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str = "ai_ops"
    postgres_user: str = "ai_ops_user"
    postgres_password: str = "ai_ops_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
