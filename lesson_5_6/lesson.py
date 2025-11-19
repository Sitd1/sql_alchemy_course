# работа в Core

from sqlalchemy import create_engine, Integer, String, ForeignKey, select, MetaData, Column, Table, insert
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.sql import or_, and_

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('name', String(30)),
    Column('fullname', String(60)),
)

address_table = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('email_address', String(50)),
    Column('user_id', Integer, ForeignKey('users.id')),
)

# ------------------------------------------------------------
# --- INSERT
# ------------------------------------------------------------

# # создаем таблицы
# with engine.connect() as connection:
#     metadata.create_all(engine)
# from sqlalchemy.dialects import postgresql, sqlite
#
#     # insert
#     # есть диалектовый инсерты
#     # сейчас мы создаем и записываем в переменную, в бд не отправляем
#     stmt = insert(user_table).values(name='Test', fullname='Test Test')
#     print(stmt.compile(bind=engine, dialect=sqlite.dialect()))
#     print(stmt.compile(bind=engine, dialect=postgresql.dialect()))
#     # 2025-11-13 10:45:05,115 INFO sqlalchemy.engine.Engine [no key 0.00002s] ()
#     # 2025-11-13 10:45:05,115 INFO sqlalchemy.engine.Engine COMMIT
#     # INSERT INTO users (name, fullname) VALUES (?, ?)
#     # INSERT INTO users (name, fullname) VALUES (%(name)s, %(fullname)s) RETURNING users.id


# with engine.connect() as connection:
#     metadata.create_all(engine)
#     stmt = insert(user_table).values(name='Test', fullname='Test Test')
#     sqlite_stmt = stmt.compile(engine, dialect=sqlite.dialect())
#     postgresql_stmt = stmt.compile(engine, dialect=postgresql.dialect())
#     print(sqlite_stmt.params)
#     print(postgresql_stmt.params)
#     # 2025-11-13 10:49:50,837 INFO sqlalchemy.engine.Engine [no key 0.00002s] ()
#     # 2025-11-13 10:49:50,837 INFO sqlalchemy.engine.Engine COMMIT
#     # {'name': 'Test', 'fullname': 'Test Test'}
#     # {'name': 'Test', 'fullname': 'Test Test'}




# with engine.begin() as conn: # type: Connection
#     # engine.connect() — "дай соединение".
#     # engine.begin() — "дай соединение и начни транзакцию с автокоммитом".
#     result = conn.execute(sqlite_stmt)
#     # print(result.inserted_primary_key)

metadata.create_all(engine)
stmt = insert(user_table).values(name='Test', fullname='Test Test')
stmt_wo_values = insert(user_table)
sqlite_stmt = stmt.compile(engine, dialect=sqlite.dialect())

with engine.begin() as conn: # type: Connection
    # engine.connect() — "дай соединение".
    # engine.begin() — "дай соединение и начни транзакцию с автокоммитом".
    result = conn.execute(
        stmt_wo_values,
        parameters=[
            {'name': 'Test1', 'fullname': 'Test1 Full'},
            {'name': 'Test2', 'fullname': 'Test2 Full'},
            {'name': 'Test3', 'fullname': 'Test3 Full'},
            {'name': 'Test4', 'fullname': 'Test4 Full'},
        ]
    )
    # 2025-11-13 11:01:53,360 INFO sqlalchemy.engine.Engine INSERT INTO users (name, fullname) VALUES (?, ?)
    # 2025-11-13 11:01:53,360 INFO sqlalchemy.engine.Engine [generated in 0.00005s] [('Test1', 'Test1 Full'), ('Test2', 'Test2 Full'), ('Test3', 'Test3 Full'), ('Test4', 'Test4 Full')]
    # алхимия вызывает параметры по одному
    # есть негативные последствия:
    # мы не сможем определить с помощью Core
    # балк инсерт
    # В ORM bulk insert делается с помощью Core, то есть нет какого-то своего механизма, мы используем модели как таблицы и делаем всё также


# ------------------------------------------------------------
# --- INSERT
# ------------------------------------------------------------
with engine.begin() as conn:
    # user_table.c.name - user_table - таблица, c - коллекция столбцов, name - название поля

    # result = conn.execute(
    #     select(user_table).where(user_table.c.name == 'Test1')
    # )
    # print(result.all())
    #

    # ------------------------------------------------------------
    # --- AND
    # ------------------------------------------------------------
    # result = conn.execute(
    #     select(user_table).where(user_table.c.name.startswith('Test'), user_table.c.fullname.contains('3'))
    # )
    # print(result.all())
    # # and_(user_table.c.name.startswith('Test'), user_table.c.fullname.contains('3'))

    # ------------------------------------------------------------
    # --- OR from sqlalchemy.sql import or_, and_
    # ------------------------------------------------------------
    #
    # result = conn.execute(
    #     select(user_table).where(or_(user_table.c.name.startswith('Test'), user_table.c.fullname.contains('3')))
    # )
    # print(result.all())

    # result = conn.execute(
    #     select(
    #         user_table.c.id,
    #         user_table.c.name
    #     )
    #         .where(
    #             or_(
    #                 user_table.c.name.startswith('Test2'),
    #                 user_table.c.fullname.contains('3')
    #             )
    #     )
    # )
    # print(result.all())

    # ------------------------------------------------------------
    # --- IN
    # ------------------------------------------------------------

    result = conn.execute(
        select(user_table.c.id,)
            .where(
                user_table.c.id.in_([1, 2])
        )
    )

    print(result.mappings().all())
    # ------------------------------------------------------------
    # --- mappings -> возврат в виде словарей
    # ------------------------------------------------------------

    result = conn.execute(
        select(user_table.c.id,)
            .where(
                user_table.c.id.in_([1, 2])
        )
    )

    print(result.mappings().all())
    lgs = '''
    2025-11-13 12:40:38,655 INFO sqlalchemy.engine.Engine SELECT users.id 
    FROM users 
    WHERE users.id IN (?, ?)
    2025-11-13 12:40:38,655 INFO sqlalchemy.engine.Engine [generated in 0.00005s] (1, 2)
    [{'id': 1}, {'id': 2}] 
    '''


