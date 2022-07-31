from typing import Union, Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator, BaseConfig


class Settings(BaseSettings):
    API_VERSION = "v1"

    # docker host ip
    HOST_IP = 'host.docker.internal'

    # DATABASE
    DB_USER: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    # built from the db pieces
    DB_URL: Optional[PostgresDsn] = None

    @validator("DB_URL", pre=True)
    def build_db_url(cls, current_value: Optional[Any], values: Dict) -> Any:
        """ build postgres connection string """
        if isinstance(current_value, str):
            return current_value

        return PostgresDsn.build(
            scheme="postgres",
            host=values.get("DB_HOST"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            path="/" + values.get("DB_NAME", "")
        )

    class Config(BaseConfig):
        case_sensitive = True
        env_file = ".env"


settings = Settings()
