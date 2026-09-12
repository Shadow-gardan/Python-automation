"""FastAPI dependencies."""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import get_task
from app.database import get_db


def get_task_or_404(task_id: int, database: Session = Depends(get_db)):
    """Resolve a task ID or raise a consistent 404 response."""
    task = get_task(database, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


__all__ = ["get_db", "get_task_or_404"]
