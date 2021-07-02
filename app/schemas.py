from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    priority_id: str
    due_date: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    class Config:
        orm_mode = True

    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
