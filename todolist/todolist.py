# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

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


class ToDoList:
    def __init__(self):
        self.today_date = datetime.today()
        self.current_short_month = self.today_date.strftime('%b')
        self.main_menu()

    def main_menu(self):
        while True:
            print("1) Today's tasks")
            print("2) Week's tasks")  # prints all tasks for 7 days from today.
            print("3) All tasks")  # prints all tasks sorted by deadline.
            print("4) Add task")
            print("0) Exit")

            menu_choice = input()

            if menu_choice == "1":
                self.today_tasks()
            elif menu_choice == '2':
                self.week_tasks()
            elif menu_choice == '3':
                self.all_tasks()
            elif menu_choice == '4':
                self.add_task()
            elif menu_choice == '0':  # Exit
                print()
                print('Bye!')
                exit()
            else:
                print('Invalid menu entry')
                print()

    # Today's tasks: print all today's tasks
    def today_tasks(self):
        self.rows = session.query(Task).filter(Task.deadline == self.today_date.date()).all()

        print()
        print(f'Today {self.today_date.day} {self.current_short_month}:')
        if self.rows:
            row_num = 1
            for self.row in self.rows:
                print(f"{row_num}. {self.row.task}")
                row_num += 1
        else:
            print('Nothing to do!')
        print()

    @staticmethod
    def add_task():
        print()
        print('Enter task')
        user_task = input()
        print('Enter deadline')

        # return datetime corresponding to user deadline
        user_deadline = input()
        task_deadline = datetime.strptime(user_deadline, '%Y-%m-%d')

        # add task here
        new_task = Task(task=user_task, deadline=task_deadline)
        session.add(new_task)
        session.commit()

        print('The task has been added')
        print()

    # Week's tasks: prints all tasks for 7 days from today.
    def week_tasks(self):
        pass
        # self.rows = session.query(Task)
        # print()
        # print(f'Today {self.today_date.day} {self.short_month}:')
        # if self.rows:
        #     for self.row in self.rows:
        #         print(f"{self.row.id}. {self.row.task}")
        # else:
        #     print('Nothing to do!')
        # print()

    # All tasks: prints all tasks sorted by deadline.
    def all_tasks(self):
        self.rows = session.query(Task).order_by(Task.deadline).all()

        print()
        print('All tasks:')
        if self.rows:
            row_num = 1
            for self.row in self.rows:
                self.short_month = self.row.deadline.strftime('%b')
                print(f"{row_num}. {self.row.task}. {self.row.deadline.day} {self.short_month}")
                row_num += 1
        else:
            print('Nothing to do!')
        print()


if __name__ == '__main__':
    # task = Task()
    to_do_list = ToDoList()
