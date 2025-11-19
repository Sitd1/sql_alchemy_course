from sqlalchemy import create_engine, text, Connection, MetaData, Table, Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# будет содержать информацию о самих таблицах
metadata = MetaData() # один объект отвечаем за одну БД

user_table = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', BigInteger, unique=True), # в разных БД под капотом будет по разному
    Column('full_name', String(50)),
)

address = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user.user_id')), # таблица.столбец
    Column('email', String(50), nullable=False),
)


# создаем все таблицы для мелких проектов
metadata.create_all(engine)
metadata.drop_all(engine)












#
# (sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % uv run -m lesson_03.lesson_03
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user") FixMe <------ Эта штука проверяет наличие таблиц, если не пройдет будет Rollback
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("user")
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("addresses")
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-11-12 16:46:58,096 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("addresses")
# 2025-11-12 16:46:58,097 INFO sqlalchemy.engine.Engine [raw sql] ()
# 2025-11-12 16:46:58,097 INFO sqlalchemy.engine.Engine
# CREATE TABLE user (
#         id INTEGER NOT NULL,
#         user_id BIGINT,
#         full_name VARCHAR(50),
#         PRIMARY KEY (id),
#         UNIQUE (user_id)
# )
#
#
# 2025-11-12 16:46:58,097 INFO sqlalchemy.engine.Engine [no key 0.00002s] ()
# 2025-11-12 16:46:58,097 INFO sqlalchemy.engine.Engine
# CREATE TABLE addresses (
#         id INTEGER NOT NULL,
#         user_id BIGINT,
#         email VARCHAR(50) NOT NULL,
#         PRIMARY KEY (id),
#         FOREIGN KEY(user_id) REFERENCES user (user_id)
# )



#
# with Session(engine) as session:
#     query = text('insert into some_table (x, y) values (:x, :y)')
#     session.execute(
#         query,
#         [
#             {'x': 10, 'y': 100},
#             {'x': 5, 'y': 7},
#         ]
#     )
#     session.commit()
#
#
# with Session(engine) as session:
#     query = text('select  x, y from some_table ORDER BY x')
#     result = session.execute(query)
#     for row in result:
#         print(row.x, row.y)
