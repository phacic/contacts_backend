from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models import User, Contact


UserSchema = pydantic_model_creator(User, name="User")
UserCreateSchema = pydantic_model_creator(User, name="UserCreateSchema", exclude_readonly=True)
