from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-this-to-a-long-random-secret"
    database_path: str = "pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    access_token_expire_minutes: int = 1440
    max_image_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
