from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, project_id: int) -> Project | None:
        result = await db.execute(select(Project).filter(Project.id == project_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Project]:
        result = await db.execute(select(Project).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, project_in: ProjectCreate) -> Project:
        db_project = Project(**project_in.model_dump())
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project

    @staticmethod
    async def update(db: AsyncSession, db_project: Project, project_in: ProjectUpdate) -> Project:
        update_data = project_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        await db.commit()
        await db.refresh(db_project)
        return db_project

    @staticmethod
    async def delete(db: AsyncSession, db_project: Project) -> None:
        await db.delete(db_project)
        await db.commit()