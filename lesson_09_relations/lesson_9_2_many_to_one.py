# Relation ship - фича ORM
# На уровне БД этой связи еще не существует
'''
    Один пользователь с несколькими адресами
'''

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, select, inspect, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, Mapper
from sqlalchemy.inspection import inspect

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

session = Session(bind=engine)

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


    address: Mapped[list["Address"]] = relationship(back_populates="user", uselist=True)  #  uselist=True - Many to one

    def __repr__(self):
        return f"<User: {self.id}: {self.name}>"


class Address(Base):
    __tablename__ = "address"

    email: Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="address", uselist=False)  # uselist=False - one to one
    user_fk: Mapped["User"] = mapped_column(ForeignKey("users.id"))


    def __repr__(self):
        return f"<Address: {self.email=}: {self.user_fk}>"


Base.metadata.create_all(engine)


user = User(id=1, name="Test", age=30)

address1 = Address(email="test1@test.com")
address2 = Address(email="test2@test.com")

user.address.append(address1)  # address.user = user
user.address.append(address2)

session.add(user)  # добавляем только user
session.commit()


# users = session.scalars(
#     select(User)
# ).all()
# addresses = session.scalars(
#     select(Address)
# ).all()

# print('-' * 100)
# print(users)
# print('-' * 100)
# print(addresses)
# print('-' * 100)

# Ленивая загрузки
user = session.scalar(select(User))

print('-' * 100)
print(user)
print('-' * 100)
print(user.address)
print('-' * 100)

# недостатки N + 1 (1 + N)
# вместо одного запроса возникает (1 + N) запросов
