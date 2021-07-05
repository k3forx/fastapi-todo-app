import io
from datetime import date, datetime

import pandas as pd
from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal, engine
from app.models import Task

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
    tasks_priorities = crud.get_all_todo_tasks(db)
    return templates.TemplateResponse(
        "todo-tasks-list.tmpl",
        {"request": request, "tasks_priorities": tasks_priorities, "calc_remaining_days": calc_remaining_days},
    )


@app.get("/completed-tasks", response_class=HTMLResponse)
def show_all_completed_tasks(request: Request, db: Session = Depends(get_db)):
    tasks_priorities = crud.get_all_done_tasks(db)
    return templates.TemplateResponse(
        "done-tasks-list.tmpl",
        {"request": request, "tasks_priorities": tasks_priorities, "calc_remaining_days": calc_remaining_days},
    )


@app.get("/tasks/new", response_class=HTMLResponse)
def show_create_new_task(request: Request):
    return templates.TemplateResponse("task-new.tmpl", {"request": request})


@app.post("/tasks/new")
def create_new_task(
    title: str = Form(...),
    description: str = Form(...),
    priority_id_str: str = Form(...),
    due_date_str: str = Form(...),
    db: Session = Depends(get_db),
):
    task = Task(
        title=title,
        description=description,
        priority_id=int(priority_id_str),
        due_date=datetime.strptime(due_date_str, "%Y-%m-%d"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_disabled=False,
    )
    crud.create_new_task(db, task)
    return RedirectResponse(url="/tasks", status_code=303)


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def show_task_by_id(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    return templates.TemplateResponse("task-edit.tmpl", {"request": request, "task": task})


@app.post("/tasks/{task_id}")
def edit_task_by_id(
    task_id: int,
    title: str = Form(...),
    description: str = Form(...),
    priority_id_str: str = Form(...),
    due_date_str: str = Form(...),
    db: Session = Depends(get_db),
):
    updated_task = {
        "title": title,
        "description": description,
        "priority_id": int(priority_id_str),
        "due_date": datetime.strptime(due_date_str, "%Y-%m-%d"),
        "updated_at": datetime.now(),
    }

    crud.update_task_by_id(db, task_id, updated_task)
    return RedirectResponse(url="/tasks", status_code=303)


@app.put("/tasks/{task_id}/completed")
def update_task_as_completed(task_id: int, db: Session = Depends(get_db)):
    completed_date = datetime.now()
    crud.update_task_completed_time(db, task_id, {"completed_at": completed_date})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


@app.put("/tasks/{task_id}/uncompleted")
def update_task_as_uncompleted(task_id: int, db: Session = Depends(get_db)):
    crud.update_task_completed_time(db, task_id, {"completed_at": None})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


@app.put("/tasks/{task_id}/disabled")
def disable_task_by_id(task_id: int, db: Session = Depends(get_db)):
    crud.disabled_task(db, task_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


@app.get("/tasks/download/todo")
def download_todo_tasks():
    sql = """
        SELECT
            t.id,
            p.priority,
            t.title,
            t.description,
            t.due_date,
            t.created_at,
            t.updated_at
        FROM
            tasks AS t
        LEFT JOIN
            priorities AS p
        ON
            t.priority_id = p.id
        WHERE
            t.completed_at IS NULL
            AND
                t.is_disabled = 0
        ORDER BY
            t.priority_id ASC, t.due_date ASC;
    """
    df = pd.read_sql_query(sql=sql, con=engine)
    stream = io.StringIO()
    df.to_csv(stream)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    response.headers["Content-Disposition"] = f"attachment; filename={current_datetime}_todo_tasks.csv"
    return response


@app.get("/tasks/download/completed")
def download_completed_tasks():
    sql = """
        SELECT
            t.id,
            p.priority,
            t.title,
            t.description,
            t.due_date,
            t.created_at,
            t.updated_at
        FROM
            tasks AS t
        LEFT JOIN
            priorities AS p
        ON
            t.priority_id = p.id
        WHERE
            t.completed_at IS NOT NULL
            AND
                t.is_disabled = 0
        ORDER BY
            t.priority_id ASC, t.due_date ASC;
    """
    df = pd.read_sql_query(sql=sql, con=engine)
    stream = io.StringIO()
    df.to_csv(stream)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    response.headers["Content-Disposition"] = f"attachment; filename={current_datetime}_completed_tasks.csv"
    return response
