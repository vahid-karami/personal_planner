from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.task import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    deadline: datetime | None = None
    estimated_duration_minutes: int = 30
    tags: list[str] = Field(default_factory=list)
    project_id: int | None = None
    parent_id: int | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    deadline: datetime | None = None
    estimated_duration_minutes: int | None = None
    tags: list[str] | None = None
    project_id: int | None = None
    parent_id: int | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)