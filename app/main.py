from datetime import date

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calc_remaining_days(due_date: date):
    current_date = date.today()
    return (due_date - current_date).days


@app.get("/tasks", response_class=HTMLResponse)
def show_all_tasks(request: Request, db: Session = Depends(get_db)):
    tasks_priorities = crud.get_all_tasks(db)
    return templates.TemplateResponse(
        "tasks-list.tmpl",
        {"request": request, "tasks_priorities": tasks_priorities, "calc_remaining_days": calc_remaining_days},
    )


@app.get("/tasks/new", response_class=HTMLResponse)
def create_new_task(request: Request):
    print("create new task")
    return templates.TemplateResponse("task-new.tmpl", {"request": request})


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def show_task_by_id(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    return templates.TemplateResponse("task-edit.tmpl", {"request": request, "task": task})
