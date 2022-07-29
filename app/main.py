from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings
from app.core import app_logger


app = FastAPI(title="Contacts App", description="A contacts with both REST and GraphQL endpoints.")

# register tortoise orm
app_logger.debug("registering tortoise orm")
register_tortoise(
    app=app, config=settings.TORTOISE_ORM, add_exception_handlers=True
)
