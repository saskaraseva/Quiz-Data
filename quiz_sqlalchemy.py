import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String


# метаданные - инф. о бд (например инф. о таблицах и столбцах)
meta = MetaData()

# создаем таблицу questions
questions = Table('Questions', meta,
                  Column('group_id', Integer, primary_key=True),
                  Column('group_name', String(30), nullable=False),
                  Column('question_id', Integer, nullable=False),
                  Column('question', String(70), nullable=False),
                  Column('answer', String(70)))