from database import Base
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String


class Priority(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String(1000), nullable=False)
    priority_id = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    is_disabled = Column(Boolean, nullable=False)
