from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.api.v1.endpoints import projects, tasks

app = FastAPI(
    title="Personal AI Planner",
    description="My Second Brain and Task Manager",
    version="1.0.0",
    # If your settings has API_V1_STR, you can use it here instead of hardcoding
)

# Register the V1 API router
app.include_router(api_router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "ok", "message": "AI Planner is online"}