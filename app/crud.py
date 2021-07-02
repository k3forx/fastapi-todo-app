from sqlalchemy.orm import Session

from app.models import Priority, Task


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(db: Session):
    return db.query(Task, Priority).outerjoin(Priority, Task.priority_id == Priority.id).all()


def create_new_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    return


def update_task_by_id(db: Session, task_id: int, updated_task: dict):
    db.query(Task).filter(Task.id == task_id).update(updated_task)
    db.commit()
    return
