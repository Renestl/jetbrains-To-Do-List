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
        self.tasks = {}
        self.main_menu()

    def main_menu(self):
        while True:
            print("1) Today's tasks")  # prints all tasks for today.
            print("2) Week's tasks")  # prints all tasks for 7 days from today.
            print("3) All tasks")  # prints all tasks sorted by deadline.
            print("4) Missed tasks")  # prints all tasks whose deadline was missed, that is, tasks whose deadline date is earlier than today's date.
            print("5) Add task")  # deletes the chosen task. Print 'Nothing to delete' if the tasks list is empty.
            print("6) Delete task")
            print("0) Exit")

            menu_choice = input()

            if menu_choice == "1":
                self.today_tasks()
            elif menu_choice == '2':
                self.week_tasks()
            elif menu_choice == '3':
                print()
                print('All tasks:')
                self.all_tasks()
            elif menu_choice == '4':
                self.missed_tasks()
            elif menu_choice == '5':
                self.add_task()
            elif menu_choice == '6':
                self.delete_task()
            elif menu_choice == '0':  # Exit
                print()
                print('Bye!')
                exit()
            else:
                print('Invalid menu entry')
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

    def delete_task(self):
        print()
        print('Choose the number of the task you want to delete:')

        # populate or update self.tasks dictionary and print task list
        self.all_tasks()

        del_task = input()
        task_id = self.tasks[del_task]['id']

        # delete a specific row
        rows = session.query(Task).filter(Task.id == task_id)
        deleted_task = rows[0]  # in case rows is not empty
        session.delete(deleted_task)
        session.commit()

        print('The task has been deleted!')
        print()

    # Today's tasks: print all today's tasks
    def today_tasks(self):
        rows = session.query(Task).filter(Task.deadline == self.today_date.date()).all()

        print()
        print(f'Today {self.today_date.day} {self.current_short_month}:')
        if rows:
            row_num = 1
            for row in rows:
                print(f"{row_num}. {row.task}")
                row_num += 1
        else:
            print('Nothing to do!')
        print()

    # Week's tasks: prints all tasks for 7 days from today.
    def week_tasks(self):
        week_ends = self.today_date + timedelta(days=6)
        rows = session.query(Task).filter(Task.deadline.between((self.today_date - timedelta(days=1)), week_ends)).order_by(Task.deadline)
        filtered_tasks = {}
        print()

        # Create dictionary containing current week
        for i in range(7):
            day = self.today_date + timedelta(days=i)
            filtered_tasks[day.strftime('%A')] = {'date': day.strftime('%d'), 'month': day.strftime('%b'), 'task': []}

        # Append tasks to current weeks task dictionary
        for row in rows:
            filtered_tasks[row.deadline.strftime('%A')]['task'].append(row.task)

        # Print out tasks
        for day, details in filtered_tasks.items():
            if len(details['task']) == 0:
                print(f"{day} {details['date']} {details['month']}:")
                print('Nothing to do!')
                print()
            else:
                row_num = 1
                print(f"{day} {details['date']} {details['month']}:")
                for item in details['task']:
                    print(f"{row_num}. {item}")
                    row_num += 1
                print()

    # @staticmethod
    # All tasks: prints all tasks sorted by deadline.
    def all_tasks(self):
        rows = session.query(Task).order_by(Task.deadline).all()

        if rows:
            row_num = 1
            for row in rows:
                short_month = row.deadline.strftime('%b')
                print(f"{row_num}. {row.task}. {row.deadline.day} {short_month}")
                self.tasks[f'{row_num}'] = {'id': row.id, 'task': row.task, 'date': row.deadline.day, 'month': row.deadline.month}
                row_num += 1
        else:
            print('Nothing to do!')
        print()

    def missed_tasks(self):
        rows = session.query(Task).filter(Task.deadline <= self.today_date).order_by(Task.deadline)

        print()
        print('Missed tasks:')
        if rows:
            row_num = 1
            for row in rows:
                short_month = row.deadline.strftime('%b')
                print(f"{row_num}. {row.task}. {row.deadline.day} {short_month}")
                row_num += 1
        else:
            print("Nothing is missed!")
        print()


if __name__ == '__main__':
    to_do_list = ToDoList()
