from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Automatically calculate the absolute path to the root folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "planner.db"

# .as_posix() forces forward slashes (/) which SQLAlchemy requires, even on Windows
SQLITE_URL = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal AI Planner"
    DATABASE_URL: str = SQLITE_URL
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

settings = Settings()