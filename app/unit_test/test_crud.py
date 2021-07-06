import unittest
from datetime import date, datetime

from crud import (
    create_new_task,
    disabled_task,
    get_all_completed_tasks,
    get_all_todo_tasks,
    get_task_by_id,
    update_task_by_id,
    update_task_completed_time,
)
from models import Priority, Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCrud(unittest.TestCase):
    def setUp(self):
        SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        self.db = TestingSessionLocal()
        self.priority_high = Priority(priority="high", created_at=datetime.now(), updated_at=datetime.now())
        self.db.add(self.priority_high)
        self.priority_low = Priority(priority="low", created_at=datetime.now(), updated_at=datetime.now())
        self.db.add(self.priority_low)
        self.todo_task_first = Task(
            title="first_todo_title",
            description="first_todo_description",
            priority_id=1,
            due_date=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_disabled=0,
        )
        self.db.add(self.todo_task_first)
        self.todo_task_second = Task(
            title="second_todo_title",
            description="second_todo_description",
            priority_id=1,
            due_date=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_disabled=0,
        )
        self.db.add(self.todo_task_second)
        self.completed_task_first = Task(
            title="first_completed_title",
            description="first_completed_description",
            priority_id=1,
            due_date=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=datetime.now(),
            is_disabled=0,
        )
        self.db.add(self.completed_task_first)
        self.db.commit()

    def test_get_task_by_id(self):
        task_id = 1
        actual = get_task_by_id(self.db, task_id)
        assert isinstance(actual, Task)
        assert actual.id == 1

    def test_all_todo_tasks(self):
        attributes = ["id", "title", "description", "priority", "due_date"]
        actual = get_all_todo_tasks(self.db)
        for result in actual:
            for attr in attributes:
                assert hasattr(result, attr)

    def test_get_all_completed_tasks(self):
        actual = get_all_completed_tasks(self.db)
        for result in actual:
            assert result.completed_at is not None

    def test_create_new_task(self):
        task = Task(
            title="some title",
            description="some description",
            priority_id=1,
            due_date=date.today(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_disabled=False,
        )
        actual = create_new_task(self.db, task)
        assert actual is None

    def test_update_task_by_id(self):
        task_id = 1
        updated_title = "updated title"
        updated_task = {"title": updated_title}
        actual = update_task_by_id(self.db, task_id, updated_task)
        task = get_task_by_id(self.db, task_id)
        assert actual is None
        assert task.title == updated_title

    def test_update_task_completed_time(self):
        task_id = 1
        now = datetime.now()
        completed_date = {"completed_at": now}
        actual = update_task_completed_time(self.db, task_id, completed_date)
        task = get_task_by_id(self.db, task_id)
        assert actual is None
        assert task.completed_at == now

    def test_disabled_task(self):
        task_id = 1
        actual = disabled_task(self.db, task_id)
        task = get_task_by_id(self.db, task_id)
        assert actual is None
        assert task.is_disabled
