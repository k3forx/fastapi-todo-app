from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    f"""mysql+pymysql://{getenv("MYSQL_USER")}:{getenv("MYSQL_PASSWORD")}@"""
    + f"""{getenv("MYSQL_HOST")}:3306/{getenv("MYSQL_DATABASE")}"""
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
