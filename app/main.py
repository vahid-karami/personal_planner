# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Personal AI Planner",
    description="Backend API for an agentic personal planner and second brain.",
    version="0.1.0",
)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Planner API is running", "status": "healthy"}