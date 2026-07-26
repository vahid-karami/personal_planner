from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.repositories.task_repository import TaskRepository

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await TaskRepository.get_all(db, skip=skip, limit=limit)

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