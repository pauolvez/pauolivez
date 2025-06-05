from fastapi import APIRouter

from . import auth, products, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(users.router)
