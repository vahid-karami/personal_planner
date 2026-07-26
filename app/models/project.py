from datetime import datetime
from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6")
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    # The string "Task" is used to avoid circular imports.
    # cascade="all, delete-orphan" means if a project is deleted, its tasks are too.
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    
    # Assuming you also have a Note model based on your __init__.py
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="project", cascade="all, delete-orphan"
    )