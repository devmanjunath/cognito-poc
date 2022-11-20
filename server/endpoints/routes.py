from fastapi import APIRouter
from server.endpoints.user import routes as user_routes
from server.endpoints.s3 import routes as s3_routes

routers = APIRouter()

routers.include_router(user_routes, prefix="/v1")
routers.include_router(s3_routes, prefix="/v1")
