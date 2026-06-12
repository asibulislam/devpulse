from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DevPulse"
    debug: bool = False
    database_url: str
    secret_key: str
    github_token: str = ""

    class Config:
        env_file = ".env"

settings = Settings()