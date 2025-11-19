# Стратегия загрузки
# lazy load (не работает с async, он идет по умолчанию)
# selectinload - самый предпочтительный при one to many
# Joined - передает один запрос с присоединением
# Явный JOIN и жадная загрузка (Eager load)
# address: Mapped[list["Address"]] = relationship(
#     back_populates="user",
#     uselist=True,
#     lazy="selectin"  # True или что-то другое ("selectin")
# )


'''
    Один пользователь с несколькими адресами
'''

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

session = Session(bind=engine)

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


    address: Mapped[list["Address"]] = relationship(
        back_populates="user",
        uselist=True,
        lazy="selectin" # True или что-то другое ("selectin")
    )

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


user = session.scalar(select(User))
print(user)
print(user.address)
