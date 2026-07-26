from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await ProjectRepository.create(db=db, project_in=project_in)


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ProjectRepository.get_all(db=db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await ProjectRepository.get_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_in: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    project = await ProjectRepository.get_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await ProjectRepository.update(db=db, db_project=project, project_in=project_in)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await ProjectRepository.get_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await ProjectRepository.delete(db=db, db_project=project)
    return None