from sqlalchemy.orm import Session

from app.models import Priority, Task


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(db: Session):
    return db.query(Task, Priority).outerjoin(Priority, Task.priority_id == Priority.id).all()


def get_all_priorities(db: Session):
    return db.query(Priority).all()
