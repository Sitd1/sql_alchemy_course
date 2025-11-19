from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Mapped, sessionmaker, DeclarativeBase
from sqlalchemy.testing.schema import mapped_column
from lesson_10_alembic.settings import DATABASE_URL




# print(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    metadata = MetaData()

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
