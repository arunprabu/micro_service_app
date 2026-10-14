from fastapi import APIRouter

from app.api.v1 import balance, statements

api_router = APIRouter()
api_router.include_router(statements.router)
api_router.include_router(balance.router)
