"""Task CRUD and filtering endpoints."""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.dependencies import get_task_or_404
from app.logging_config import logger
from app.models import Task
from app.schemas import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(task_data: TaskCreate, database: Session = Depends(get_db)) -> Task:
    """Create a task with validated status and priority values."""
    task = crud.create_task(database, task_data)
    logger.info("Created task id=%s", task.id)
    return task


@router.get("", response_model=list[TaskResponse], summary="List tasks")
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status", description="Filter by task status"),
    priority: TaskPriority | None = Query(default=None, description="Filter by task priority"),
    skip: int = Query(default=0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Maximum tasks to return"),
    database: Session = Depends(get_db),
) -> list[Task]:
    """List tasks with optional status, priority, and pagination filters."""
    return crud.get_tasks(database, status_filter.value if status_filter else None, priority.value if priority else None, skip, limit)


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task")
def read_task(task: Task = Depends(get_task_or_404)) -> Task:
    """Return one task by ID."""
    return task


@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
def update_task(
    task_data: TaskUpdate,
    task: Task = Depends(get_task_or_404),
    database: Session = Depends(get_db),
) -> Task:
    """Update any provided task fields."""
    updated = crud.update_task(database, task, task_data)
    logger.info("Updated task id=%s", updated.id)
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task: Task = Depends(get_task_or_404), database: Session = Depends(get_db)) -> Response:
    """Delete a task and return an empty 204 response."""
    task_id = task.id
    crud.delete_task(database, task)
    logger.info("Deleted task id=%s", task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
