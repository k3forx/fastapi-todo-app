import unittest
from datetime import date, datetime

import pytest
from database import Base
from fastapi import status
from fastapi.testclient import TestClient
from main import app, get_db
from models import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        print("add task")
        db.add(
            Task(
                title="title 1",
                description="description 1",
                priority_id=1,
                due_date=date.today(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_disabled=0,
            )
        )
        db.commit()
        print("commit")
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


# FIXME: https://github.com/encode/starlette/issues/472
@pytest.fixture
def exclude_middleware():
    user_middleware = app.user_middleware.copy()
    app.user_middleware = []
    app.middleware_stack = app.build_middleware_stack()
    yield
    app.user_middleware = user_middleware
    app.middleware_stack = app.build_middleware_stack()


def test_hello_world():
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == status.HTTP_200_OK


def test_show_all_tasks(exclude_middleware):
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
