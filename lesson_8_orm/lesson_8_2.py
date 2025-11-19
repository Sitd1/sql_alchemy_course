# ORM part 2
# Группы изменений
# new - session.new - коллекция, IdentitySet, спец класс,
#     который создается Алхимией, множество в ОРМ,
#     где в качестве уникальности используется не хэш, как это обычно происходит в случае set,
#     а при помощи проверки первичного ключа
# dirty (persistent)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, Mapper
from sqlalchemy.inspection import inspect

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


Base.metadata.create_all(engine)

user = User(id=1, name='Test', age=30)
session.add(user)
session.flush()
user.age = 25

print(user in session.dirty)

# ORM (unit of work) не делает лишних действий
# Если убрать предыдущий строка 31  flush(), то запрос будет не UPDATE, а INSERT
""" sqlalchemy.engine.Engine INSERT INTO users (id, name, age) VALUES (?, ?, ?)"""
# А если оставить строка 31, то будет:
""" sqlalchemy.engine.Engine UPDATE users SET age=? WHERE users.id = ?"""

session.flush()

print(session.new)


# ------------------------------------------------------------------------------------
# --- AutoFlush session = Session(engine, expire_on_commit=True, autoflush=True)
# Теперь сразу всегда делается flush (поэтому он по сути не нужен)
# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# --- Identity Map
# ------------------------------------------------------------------------------------

# session.expire_all() - # отмечает все объекты в IdentityMap устаревшими
# session.expunge_all() - # удаляет (очищает) все объекты в IdentityMap