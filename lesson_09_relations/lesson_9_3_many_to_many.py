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


    addresses: Mapped[list["Address"]] = relationship(back_populates="users", uselist=True, secondary="user_address")  #  uselist=True - Many to one

    def __repr__(self):
        return f"<User: {self.id}: {self.name}>"


class Address(Base):
    __tablename__ = "address"

    email: Mapped[str] = mapped_column(primary_key=True)

    users: Mapped[list["User"]] = relationship(back_populates="addresses", uselist=True, secondary="user_address")  # uselist=False - one to one
    # user_fk: Mapped["User"] = mapped_column(ForeignKey("users.id"))


    def __repr__(self):
        return f"<Address: {self.email=}>"

# таблица ассоциаций
class UserAddress(Base):
    __tablename__ = "user_address"
    user_fk = mapped_column(ForeignKey("users.id"), primary_key=True)
    address_fk = mapped_column(ForeignKey("address.email"), primary_key=True)

    def __repr__(self):
        return f"<UserAddress: {self.user_fk=} : {self.address_fk=}>"


Base.metadata.create_all(engine)


user1 = User(id=1, name="Test", age=30)
user2 = User(id=2, name="Test2", age=31)

address1 = Address(email="test1@test.com")
address2 = Address(email="test2@test.com")

user1.addresses.append(address1)  # address.user = user
user1.addresses.append(address2)
user2.addresses.append(address1)  # address.user = user
user2.addresses.append(address2)

session.add(user1)  # добавляем только user
session.add(user2)
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
users = session.scalars(select(User)).all()
user_secondary = session.scalars(select(UserAddress)).all()
adresses = session.scalars(select(Address)).all()

print('-' * 100)
print(users)
print('-' * 100)
# print([user.addresses for user in users])
print(adresses)
print('-' * 100)
print(user_secondary)

# недостатки N + 1 (1 + N)
# вместо одного запроса возникает (1 + N) запросов
