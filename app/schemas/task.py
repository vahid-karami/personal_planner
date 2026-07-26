from pydantic import BaseModel, Field
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    is_completed: bool = False
    due_date: datetime | None = None
    project_id: int | None = None

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    is_completed: bool | None = None
    due_date: datetime | None = None
    project_id: int | None = None

class TaskResponse(TaskBase):
    """Schema for returning task data to the client."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}