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

    TORTOISE_ORM: Optional[Dict] = None

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

    @validator("TORTOISE_ORM", pre=True)
    def build_tortoise_config(cls, current_value: Optional[Dict], values: Dict) -> Dict:
        """ build tortoise orm settings """
        if isinstance(current_value, Dict):
            return current_value

        return {
            "connections": {"default": str(values.get("DB_URL"))},
            "apps": {
                "models": {
                    "models": ["aerich.models"],
                    "default_connection": "default",
                },
            },
        }

    class Config(BaseConfig):
        case_sensitive = True
        env_file = ".env"


settings = Settings()
