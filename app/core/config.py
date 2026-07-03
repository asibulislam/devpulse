from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DevPulse"
    debug: bool = False
    database_url: str
    secret_key: str
    github_token: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()