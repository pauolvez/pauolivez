from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./kingstar.db"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AMAZON_APP_ID: str = ""  # Amazon SP-API credentials placeholder
    AMAZON_CLIENT_SECRET: str = ""
    AMAZON_REFRESH_TOKEN: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
