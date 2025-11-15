import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "llm-data-chart-api")
    ENV: str = os.getenv("ENV", "dev")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "stub")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "stub-v1")

settings = Settings()
