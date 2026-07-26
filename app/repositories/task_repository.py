from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    
    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: int) -> Task | None:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Task]:
        result = await db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, task_in: TaskCreate) -> Task:
        db_task = Task(**task_in.model_dump())
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