from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)


def today_tasks():
    print(f'\nToday {datetime.today().strftime("%e %b")}:')
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if rows:
        for cnt, row in enumerate(rows, 1):
            print(f'{cnt}. {row.task}')
    else:
        print('Nothing to do!')


def week_tasks():
    rows = session.query(Table).filter(Table.deadline + timedelta(days=7) <= datetime.today().date()).all()
    for day in range(7):
        print(f'\n{(datetime.today() + timedelta(days=day)).strftime("%A %e %b:")}')
        i = 1
        for row in rows:
            if row.deadline == (datetime.today().date() + timedelta(days=day)):
                print(f'{i}. {row.task}')
                i += 1
            else:
                continue


def all_tasks():
    print('\nAll tasks:')
    rows = session.query(Table).all()
    if len(rows) > 0:
        for cnt, row in enumerate(rows, 1):
            print(f'{cnt}. {row.task}. {row.deadline.strftime("%e %b")}')
    else:
        print('Nothing to do!')


def missed_tasks():
    print('\nMissed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    if len(rows) > 0:
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row.task}. {row.deadline.strftime("%e %b")}')
    else:
        print('Nothing is missed!')


def add_task():
    print('\nEnter task')
    new_task = input()
    print('Enter deadline')
    date = input().split('-')
    new_row = Table(task=new_task, deadline=datetime(int(date[0]), int(date[1]), int(date[2])))
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def delete_task():
    print('\nChose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) > 0:
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row.task}. {row.deadline.strftime("%e %b")}')
        which = int(input())
        to_delete = ''
        for i, row in enumerate(rows, 1):
            if i == which:
                to_delete = row.task
        query = session.query(Table).filter(Table.task == to_delete)
        session.delete(query[0])
        session.commit()
    else:
        print('Nothing to delete')


while True:
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    answer = input()
    if answer == '0':
        break
    elif answer == '1':
        today_tasks()
    elif answer == '2':
        week_tasks()
    elif answer == '3':
        all_tasks()
    elif answer == '4':
        missed_tasks()
    elif answer == '5':
        add_task()
    elif answer == '6':
        delete_task()
    else:
        print('Type in proper number')
