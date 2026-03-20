from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Quick Notes"
    APP_VERSION: str = "0.1.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8765
    DATA_DIR: Path = Path.home() / ".quicknotes"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
