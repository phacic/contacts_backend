from fastapi import APIRouter

from app.api.router.contact import router as contact_router
from app.api.router.user import router as user_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(router=contact_router, prefix="/contact")
v1_router.include_router(router=user_router, prefix="/users")
