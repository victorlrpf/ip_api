from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IP API"
    app_token: str
    chave_secreta: str = "7f3a9c2e-91ab-4c8d-bf21-9d8a7c5e12344226"
    algoritmo: str = "HS256"
    token_expiration: int = 30
    mongodb_url: str
    mongodb_db: str = "ip_tracker"
    ipwhois_base_url: str = "https://ipwhois.is"
    redis_url: str = "redis://localhost:6379/0"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()