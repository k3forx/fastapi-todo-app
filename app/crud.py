from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models import Priority, Task


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_todo_tasks(db: Session):
    return (
        db.query(Task, Priority)
        .filter(Task.completed_at.is_(None))
        .outerjoin(Priority, Task.priority_id == Priority.id)
        .order_by(asc(Task.priority_id), asc(Task.due_date))
        .all()
    )


def get_all_done_tasks(db: Session):
    return (
        db.query(Task, Priority)
        .filter(Task.completed_at.isnot(None))
        .outerjoin(Priority, Task.priority_id == Priority.id)
        .order_by(asc(Task.priority_id), asc(Task.due_date))
        .all()
    )


def create_new_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    return


def update_task_by_id(db: Session, task_id: int, updated_task: dict):
    db.query(Task).filter(Task.id == task_id).update(updated_task)
    db.commit()
    return


def update_task_completed_time(db: Session, task_id: int, completed_date: dict):
    db.query(Task).filter(Task.id == task_id).update(completed_date)
    db.commit()
    return
