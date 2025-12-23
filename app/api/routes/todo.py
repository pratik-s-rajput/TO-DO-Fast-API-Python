from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])





# ----------------------------
# CREATE TASK
# ----------------------------
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    new_task = Task(
        task_name=task.task_name,
        description=task.description,
        owner_id=1  # TEMP: hardcoded user (we’ll fix later
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ----------------------------
# GET ALL TASKS
# ----------------------------
@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


# ----------------------------
# GET SINGLE TASK
# ----------------------------
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# ----------------------------
# UPDATE TASK
# ----------------------------
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task_data.task_name is not None:
        task.task_name = task_data.task_name

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    db.commit()
    db.refresh(task)

    return task


# ----------------------------
# DELETE TASK
# ----------------------------
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None
