# работа с метаданными в ORM
# всё что для ORM будет содержаться в sqlalchemy.orm -> from sqlalchemy.orm import Session
# registry - то же самое, что metadata

from sqlalchemy import create_engine, Integer, String, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base, as_declarative, DeclarativeMeta
from sqlalchemy.orm import registry, mapped_column, Mapped, Session
from sqlalchemy.testing.pickleable import User

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# mapper_registry = registry() # старый формат
# Base = mapper_registry.generate_base() # старый формат

# print(mapper_registry)
# print(mapper_registry.metadata)

# (sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % uv run -m lesson_4.lesson
# <sqlalchemy.orm.decl_api.registry object at 0x104e917d0>
# MetaData()




# ни в коем случае не должны писать def __init__ - он уже создается автоматически
# from sqlalchemy.orm import registry
# mapper_registry = registry()
# Base = mapper_registry.generate_base()

# Все действия по созданию регистра и декларативного базиса
# могут быть объединены в один простой шаг:

# from sqlalchemy.orm import declarative_base
# Base = declarative_base()


# При этом в новых версиях алхимии
# допускается и следующий вариант создания декларативного базиса:
# from sqlalchemy.ext.declarative import as_declarative
#
#
# @as_declarative()
# class Base(object):
#     id = Column(Integer, autoincrement=True, primary_key=True)

@as_declarative()
class AbstractModel():
    # __abstract__ = True
    id = mapped_column(Integer, primary_key=True)

class UserModel(AbstractModel):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)

class AddressModel(AbstractModel):
    __tablename__ = 'addresses'
    email = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'), nullable=False)

# print(UserModel.__table__.__dict__)
# print(AddressModel.__table__.__dict__)

# print(UserModel.__table__) # noqa


with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = UserModel(id=1, name='Jack', fullname='Jack Cow')  # noqa
        session.add(user)

    with session.begin():
        res = session.execute(select(UserModel).where(UserModel.id == 1))
        user = res.scalar()

