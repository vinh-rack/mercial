from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    log_level: str = "INFO"
    log_dir: str = "logs"

    db_host: str = "localhost"
    db: str = "inventory_db"
    db_user: str = "postgres"
    db_password: str = "password"


settings = Settings()
