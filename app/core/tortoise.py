from app.core.config import settings

orm_config = {
    "connections": {"default": str(settings.DB_URL)},
    "apps": {
        "models": {
            "models": ["app.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
