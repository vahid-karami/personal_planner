@staticmethod
async def get_all(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    is_completed: bool | None = None,
    project_id: int | None = None,
    due_date_from: datetime | None = None,
    due_date_to: datetime | None = None,
    q: str | None = None,
    owner_id: int | None = None,
) -> list[Task]:
    query = select(Task).order_by(Task.id)

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
