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


class ToDoList:
    def __init__(self):
        self.task = ''


def main_menu(self):
    while True:
        print("1) Today's tasks")
        print("2) Add task")
        print("0) Exit")

        menu_choice = input()

        if menu_choice == "1":
            pass
        elif menu_choice == '2':
            pass
        elif menu_choice == '0':
            print()
            print('Bye!')
            exit()
        else:
            print('Invalid menu entry')
            print()


if __name__ == '__main__':
    task = Task()
    list = ToDoList()
