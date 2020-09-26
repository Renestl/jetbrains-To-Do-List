# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('todo.db?check_Same_thread=False')

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

Task.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def menu():
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")
