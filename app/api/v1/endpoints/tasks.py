@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    is_completed: bool | None = None,
    project_id: int | None = Query(None, ge=1),
    due_date_from: datetime | None = None,
    due_date_to: datetime | None = None,
    q: str | None = Query(None, min_length=1, description="Search in task title and description"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
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
        owner_id=current_user.id,
    )
