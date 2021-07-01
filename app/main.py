from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/tasks", response_class=HTMLResponse)
def show_all_tasks(request: Request):
    print("show todo list")
    return templates.TemplateResponse("list-task-todo.html", {"request": request})


@app.get("/tasks/new", response_class=HTMLResponse)
def create_new_task(request: Request):
    print("create new task")
    return templates.TemplateResponse("task-new.html", {"request": request})


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def show_task_by_id(request: Request):
    print("edit a task")
    return templates.TemplateResponse("task-edit.html", {"request": request})
