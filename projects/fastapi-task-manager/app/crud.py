"""Database operations for tasks."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def create_task(database: Session, task_data: TaskCreate) -> Task:
    """Create and persist a task."""
    task = Task(**task_data.model_dump())
    database.add(task)
    database.commit()
    database.refresh(task)
    return task


def get_tasks(
    database: Session,
    status: str | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Task]:
    """Return filtered, paginated tasks ordered newest first."""
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)
    return list(database.scalars(query).all())


def get_task(database: Session, task_id: int) -> Task | None:
    """Return one task or None when it does not exist."""
    return database.get(Task, task_id)


def update_task(database: Session, task: Task, task_data: TaskUpdate) -> Task:
    """Apply provided fields and persist the task update."""
    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    database.commit()
    database.refresh(task)
    return task


def delete_task(database: Session, task: Task) -> None:
    """Delete a task from the database."""
    database.delete(task)
    database.commit()
