# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column('id', Integer, primary_key=True)
    task = Column('task', String)
    deadline = Column('deadline', Date, default=datetime.today())


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()


def retrieve_tasks():
    rows = session.query(Task).all()

    print()
    print('Today:')
    if rows:
        for row in rows:
            print(f"{row.id}. {row.task}")
    else:
        print('Nothing to do!')
    print()


def add_task():
    print()
    print('Enter task')

    user_task = input()

    # add task here
    new_task = Task(task=user_task)
    session.add(new_task)
    session.commit()

    print('The task has been added')
    print()


class ToDoList:
    def __init__(self):
        self.task = ''
        self.main_menu()

    def main_menu(self):
        while True:
            print("1) Today's tasks")
            print("2) Add task")
            print("0) Exit")

            menu_choice = input()

            if menu_choice == "1":
                retrieve_tasks()
            elif menu_choice == '2':
                add_task()
            elif menu_choice == '0':
                print()
                print('Bye!')
                exit()
            else:
                print('Invalid menu entry')
                print()


if __name__ == '__main__':
    # task = Task()
    to_do_list = ToDoList()
