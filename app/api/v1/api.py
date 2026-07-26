from fastapi import APIRouter
from app.api.v1.endpoints import projects

api_router = APIRouter()

# Include the project endpoints we just wrote
api_router.include_router(projects.router)

# We will add tasks here later:
# api_router.include_router(tasks.router)