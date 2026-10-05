from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Each settings group reads the same .env, which also holds the other groups' keys, so
# unknown keys are ignored rather than rejected.
_ENV = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    """Postgres connection settings, read from DB_* variables."""

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    host: str = Field(default="db", description="Postgres host.")
    port: int = Field(default=5432, description="Postgres port.")
    name: str = Field(default="activities", description="Database name.")
    username: str = Field(default="postgres", description="Database user.")
    password: str = Field(default="postgres", description="Database password.")

    @property
    def url(self) -> str:
        """Return a psycopg2-compatible connection URL."""
        return (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class StravaSettings(BaseSettings):
    """Strava API credentials and where the OAuth tokens are cached."""

    model_config = _ENV

    client_id: str = Field(description="Strava API application client ID")
    client_secret: str = Field(description="Strava API application client secret")
    creds_path: Path = Field(
        default=Path("/app/etl/.creds"),
        description="Path to the Strava OAuth token cache file",
    )


class Settings(BaseSettings):
    """All pipeline settings; the groups are read from the environment on creation."""

    model_config = _ENV

    db: DatabaseSettings = Field(
        default_factory=DatabaseSettings, description="Postgres connection."
    )
    strava: StravaSettings = Field(
        default_factory=StravaSettings,
        description="Strava API access.",
    )
    data_in_path: Path = Field(
        default=Path("data/raw/"), description="Directory of raw activity CSVs."
    )
    data_out_path: Path = Field(
        default=Path("data/processed/"), description="Directory for processed CSVs."
    )
    tables_out_path: Path = Field(
        default=Path("data/warehouse/"),
        description="Directory for per-run dimension table CSVs.",
    )


def get_settings() -> Settings:
    """Return a Settings instance loaded from environment and .env file."""
    return Settings()
