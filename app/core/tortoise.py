from app.core.config import settings

MODEL_LIST = ["app.db.models", "aerich.models"]

orm_config = {
    "connections": {"default": str(settings.DB_URL)},
    "apps": {
        "models": {
            "models": MODEL_LIST,
            "default_connection": "default",
        },
    },
}
