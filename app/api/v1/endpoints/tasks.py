from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_completed: bool | None = None,
    project_id: int | None = Query(None, ge=1),
    due_date_from: datetime | None = None,
    due_date_to: datetime | None = None,
    q: str | None = Query(None, min_length=1, description="Search in task title and description"),
    db: AsyncSession = Depends(get_db),
):
    return await TaskRepository.get_all(
        db,
        skip=skip,
        limit=limit,
        is_completed=is_completed,
        project_id=project_id,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        q=q,
    )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await TaskRepository.create(db=db, task_in=task_in)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await TaskRepository.get_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_in: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await TaskRepository.get_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await TaskRepository.update(db=db, db_task=task, task_in=task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await TaskRepository.get_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await TaskRepository.delete(db=db, db_task=task)
    return None
