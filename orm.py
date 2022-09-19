from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

import requests

from sqlalchemy import create_engine


Base = declarative_base()

class Questions(Base):
    __tablename__ = "questions"

    group_id = Column(Integer, primary_key=True)
    group_name = Column(Text(30))
    question_id = Column(Integer)
    question = Column(Text)
    answer = Column(Text)

    def __repr__(self):
        return f"User(group_id={self.group_id!r}, group_name={self.group_name!r}, question_id={self.question_id!r}, " \
               f"question={self.question!r}, answer={self.answer!r})"


engine = create_engine("sqlite:///sqlite_python.db", echo=True, future=True)

Base.metadata.create_all(engine)

# обращаемся к эндпоинту /api/random публичного API сервиса https://jservice.io/
res = requests.get("https://jservice.io/api/random")
#print(res.status_code)
json = res.json()
a = (json[0]['category']['id'], json[0]['category']['title'], json[0]['id'], json[0]['question'], json[0]['answer'])
print(a)

# запись в бд
with Session(engine) as session:
    record = Questions(group_id =json[0]['category']['id'], group_name=json[0]['category']['title'],
                       question_id=json[0]['id'], question=json[0]['question'], answer=json[0]['answer'])

    session.add(record)
    session.commit()

# запрос из бд
session = Session(engine)
query = session.execute(
    select(Questions.group_id, Questions.group_name, Questions.question,
           Questions.answer).order_by(Questions.group_id)
).all()

print(query)


