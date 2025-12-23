from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------- CREATE --------
class TaskCreate(BaseModel):
    task_name: str
    description: Optional[str] = None


# -------- UPDATE --------
class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# -------- RESPONSE --------
class TaskResponse(BaseModel):
    id: int
    task_name: str
    description: Optional[str]
    is_completed: bool
    completed_at: Optional[datetime]=None
    created_at: datetime=None

    class Config:
        from_attributes = True
