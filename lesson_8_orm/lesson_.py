# ORM
"""
Состояния объектов в SQLAlchemy:

Transient - объект создан, но не добавлен в сессию
Pending - добавлен в сессию через add(), но еще не сохранен в БД
Persistent - синхронизирован с БД после flush() или commit()
Deleted - помечен для удаления через delete(), но еще в сессии
Detached - был в сессии, но она закрыта или объект явно удален из сессии
"""
# Objective-Relational Mapping (объектно реляционное отображение)
# Объединение работ - все изменения, которые совершаем над БД не отправляются по одиночке
# А собираются в кучу и отправляются группой
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
insp = inspect(user)


# Transient (временный)
# Pending (ожидающий)
# Persistent (персистентный)
# Deleted (удаленный)
# Detached (отсоединенный)

print('-' * 100)
print('Is transient?', insp.transient)
print('-' * 100)
print('Adding user to session')
session.add(user)
print('-' * 100)
print('Is transient?', insp.transient)
print('Is pending?', insp.pending)
print('-' * 100)
print('Flushing session')
session.flush()  # Перемещение данных из Unit of Work в сессии -> в транзакцию в БД
print('-' * 100)
print('Is transient?', insp.transient)
print('Is pending?', insp.pending)
print('Is persistent?', insp.persistent)
print('-' * 100)
print('Deleting session')
# session.delete(user)
print('*' * 100)
print('Flushing session')
# session.flush()
print('*' * 100)
print('-' * 100)

# session.commit() | session.rollback()
# session.close()
