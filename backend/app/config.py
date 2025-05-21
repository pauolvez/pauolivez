from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    openai_api_key: str  # 👈 necesaria para ScrapeGraphAI

    class Config:
        env_file = ".env"
        extra = "allow"  # 👈 permite que no falle si hay más claves en .env

settings = Settings()