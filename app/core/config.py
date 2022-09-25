from typing import Any, Dict, Optional

from pydantic import BaseConfig, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API: str = "/api"
    GRAPH_QL: str = "/graphql"

    SECRET: Optional[str] = None

    # docker host ip
    HOST_IP: Optional[str] = None

    # DATABASE
    DB_USER: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    # built from the db pieces
    DB_URL: Optional[PostgresDsn] = None

    @validator("DB_URL", pre=True)
    def build_db_url(cls, current_value: Optional[Any], values: Dict) -> Any:
        """build postgres connection string"""
        print(values)

        if isinstance(current_value, str):
            return current_value

        return PostgresDsn.build(
            scheme="postgres",
            host=values.get("DB_HOST"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            path="/" + values.get("DB_NAME", ""),
        )

    class Config(BaseConfig):
        case_sensitive = True
        env_file = ".env"


settings = Settings()
