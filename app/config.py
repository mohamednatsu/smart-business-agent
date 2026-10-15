from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Environment variables use the SBA_ prefix, e.g. SBA_DEBUG=true.
    """

    model_config = SettingsConfigDict(
        env_prefix="SBA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Smart Business Agent"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
