from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    host: str = Field(default="db")
    port: int = Field(default=5432)
    name: str = Field(default="activities")
    username: str = Field(default="postgres")
    password: str = Field(default="postgres")

    @property
    def url(self) -> str:
        """Return a psycopg2-compatible connection URL."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class StravaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    client_id: str = Field(description="Strava API application client ID")
    client_secret: str = Field(description="Strava API application client secret")
    creds_path: Path = Field(
        default=Path("/app/etl/.creds"),
        description="Path to the Strava OAuth token cache file",
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    strava: StravaSettings = Field(default_factory=StravaSettings)
    data_in_path: Path = Field(default=Path("data/raw/"))
    data_out_path: Path = Field(default=Path("data/processed/"))
    tables_out_path: Path = Field(default=Path("data/warehouse/"))


def get_settings() -> Settings:
    """Return a Settings instance loaded from environment and .env file."""
    return Settings()
