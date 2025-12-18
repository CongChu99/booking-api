from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    port: int = 8000
    database_url: str | None = None   # lấy từ env/secret manager

    class Config:
        env_file = ".env"  # .env không commit
        extra = "ignore"

settings = Settings()
