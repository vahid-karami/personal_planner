from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(
    title="Personal AI Planner",
    description="My Second Brain and Task Manager",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "ok", "message": "AI Planner is online"}