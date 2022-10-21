from fastapi import APIRouter

from apps.api.api_v1.endpoints import accuracy, login, users

api_router = APIRouter()

api_router.include_router(accuracy.router,
                          prefix="/acurracy",
                          tags=["accurancy"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, tags=["login"])
