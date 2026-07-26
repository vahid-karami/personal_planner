from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = None
    color: str = Field("#3B82F6", max_length=7)  # Hex code default


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
    color: str | None = Field(None, max_length=7)


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)