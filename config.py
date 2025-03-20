from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APPLICATION_VERSION: str = "1.0.0"
    TEST_MODE: bool = True
    DATABASE_URL: str
    ENV_MODE: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

def get_settings() -> Settings:
    return Settings()