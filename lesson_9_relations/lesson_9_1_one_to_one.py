# Relation ship - фича ORM
# На уровне БД этой связи еще не существует
"""
    У одного пользователя 1 адрес
"""

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


    address: Mapped["Address"] = relationship(back_populates="user", uselist=False)  # uselist=False - one to one

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
address = Address(email="test@test.com")
user.address = address  # address.user = user

session.add(user)  # добавляем только user
session.commit()


users = session.scalar(
    select(User)
)
addresses = session.scalar(
    select(Address)
)

print('-' * 100)
print(users)
print('-' * 100)
print(addresses)
print('-' * 100)
