from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Backend"
    debug: bool = False
    secret_key: str = "change-me-to-a-long-random-secret-key"
    environment: str = "development"

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "password"
    db_name: str = "fast_backend"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    jwt_algorithm: str = "HS256"

    openai_api_key: str = "sk-your-openai-api-key"
    openai_model: str = "gpt-4o-mini"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
