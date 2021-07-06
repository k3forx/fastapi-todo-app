from models import Priority, Task
from sqlalchemy import asc
from sqlalchemy.orm import Session


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_todo_tasks(db: Session):
    return (
        db.query(Task.id, Task.title, Task.description, Priority.priority, Task.due_date)
        .filter(Task.completed_at.is_(None), Task.is_disabled.is_(False))
        .outerjoin(Priority, Task.priority_id == Priority.id)
        .order_by(asc(Task.priority_id), asc(Task.due_date))
        .all()
    )


def get_all_completed_tasks(db: Session):
    return (
        db.query(Task.id, Task.title, Task.description, Priority.priority, Task.due_date, Task.completed_at)
        .filter(Task.completed_at.isnot(None), Task.is_disabled.is_(False))
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


def disabled_task(db: Session, task_id: int):
    db.query(Task).filter(Task.id == task_id).update({"is_disabled": True})
    db.commit()
    return
