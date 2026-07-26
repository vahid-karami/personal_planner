from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:

    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: int, owner_id: int) -> Task | None:
        result = await db.execute(
            select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_completed: bool | None = None,
        project_id: int | None = None,
        due_date_from: datetime | None = None,
        due_date_to: datetime | None = None,
        q: str | None = None,
        owner_id: int | None = None,
    ) -> list[Task]:
        query = select(Task)

        if owner_id is not None:
            query = query.filter(Task.owner_id == owner_id)

        if is_completed is not None:
            query = query.filter(Task.is_completed == is_completed)

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        if due_date_from is not None:
            query = query.filter(Task.due_date >= due_date_from)

        if due_date_to is not None:
            query = query.filter(Task.due_date <= due_date_to)

        if q:
            search_term = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term),
                )
            )

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, task_in: TaskCreate, owner_id: int) -> Task:
        db_task = Task(**task_in.model_dump(), owner_id=owner_id)
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def update(db: AsyncSession, db_task: Task, task_in: TaskUpdate) -> Task:
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def delete(db: AsyncSession, db_task: Task) -> None:
        await db.delete(db_task)
        await db.commit()
