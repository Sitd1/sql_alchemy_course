# работа в Core

from sqlalchemy import create_engine, Integer, String, ForeignKey, select, MetaData, Column, Table, insert, desc, \
    update, bindparam, delete
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.sql import or_, and_

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('first_name', String(30)),
    Column('second_name', String(60)),
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

metadata.create_all(engine)
# stmt = insert(user_table).values(first_name='Test', second_name='Test Test')
# sqlite_stmt = stmt.compile(engine, dialect=sqlite.dialect())
stmt_wo_values = insert(user_table)

with engine.begin() as conn: # type: Connection
    # engine.connect() — "дай соединение".
    # engine.begin() — "дай соединение и начни транзакцию с автокоммитом".

    conn.execute(
        stmt_wo_values,
        parameters=[
            {'first_name': 'Test1', 'second_name': 'Test1_second'},
            {'first_name': 'Test2', 'second_name': 'Test2_second'},
            {'first_name': 'Test3', 'second_name': 'Test3_second'},
            {'first_name': 'Test4', 'second_name': 'Test4_second'},
        ]
    )

    conn.execute(
        insert(address_table),
        parameters=[
            {'email_address': 'test1@yandex.ru', 'user_id': 1},
            {'email_address': 'test2@yandex.ru', 'user_id': 2},
            {'email_address': 'test3@yandex.ru', 'user_id': 3},
            {'email_address': 'test4@yandex.ru', 'user_id': 4},
        ]
    )

# ------------------------------------------------------------
# --- SELECT
# ------------------------------------------------------------

# with engine.begin() as conn:
#     result = conn.execute(
#         select(
#             user_table.c.first_name + user_table.c.first_name
#         ).where(
#             user_table.c.id.in_([1, 2])
#         )
#     )
#     print(result.mappings().all())
#     """
#     # FROM users
#     # WHERE users.id IN (?, ?)
#     # 2025-11-13 13:47:23,949 INFO sqlalchemy.engine.Engine [generated in 0.00006s] (1, 2)
#     # [{'anon_1': 'Test1Test1'}, {'anon_1': 'Test2Test2'}]
#     """
#     # появились какие-то анонимные функции

# with engine.begin() as conn:
#     result = conn.execute(
#         select(
#             (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name'),
#         ).where(
#             user_table.c.id.in_([1, 2])
#         )
#     )
#     # print(result.mappings().all())
#     for row in result:
#         print(row.full_name)


# # ------------------------------------------------------------
# # --- SELECT из разных таблиц
# # ------------------------------------------------------------
# with engine.begin() as conn:
#     # join_from и левую и правую
#     # join только правую
#     # result = conn.execute(
#     #     select(
#     #         address_table.c.email_address.label('email'),
#     #         (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
#     #     )
#     #         .where(
#     #             user_table.c.id > 1
#     #         )
#     #         .join_from(user_table, address_table)
#     # )
#     # print(result.all())
#     '''
#     #     2025-11-13 13:59:59,042 INFO sqlalchemy.engine.Engine SELECT addresses.email_address AS email, users.first_name || ? || users.first_name AS full_name
#     #     FROM users JOIN addresses ON users.id = addresses.user_id
#     #     WHERE users.id > ?
#     #     2025-11-13 13:59:59,042 INFO sqlalchemy.engine.Engine [generated in 0.00004s] (' ', 1)
#     #     [('test2@yandex.ru', 'Test2 Test2'), ('test3@yandex.ru', 'Test3 Test3'), ('test4@yandex.ru', 'Test4 Test4')]
#     '''
#     # автоматический создались блоки ON
#
#     # ------------------------------------------------------------
#     # --- SELECT из разных таблиц (ручное указание ON)
#     # ------------------------------------------------------------
#
#     # result = conn.execute(
#     #     select(
#     #         address_table.c.email_address.label('email'),
#     #         (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
#     #     )
#     #         .where(
#     #             user_table.c.id > 1
#     #         )
#     #         .join_from(user_table, address_table, onclause=and_(user_table.c.id == address_table.c.user_id))
#     # )
#     # print(result.all())
#
#     # ------------------------------------------------------------
#     # --- SELECT из разных таблиц (просто join, без join_from)
#     # ------------------------------------------------------------
#
#     result = conn.execute(
#         select(
#             address_table.c.email_address.label('email'),
#             (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
#         )
#             .where(
#                 user_table.c.id > 1
#             )
#             .join(address_table)
#     )
#     print(result.all())
#     # здесь всё происходит полностью автоматически. Даже не нужно указывать левую сторону.
#     # также есть различные методы left, outer, right
#     # .join(address_table, isouter=True)
#     # .join(address_table, full=True)
#     # full left


# ------------------------------------------------------------
# --- SELECT из разных табли ORDER BY
# ------------------------------------------------------------
# with engine.begin() as conn:
    # join_from и левую и правую
    # join только правую
    # result = conn.execute(
    #     select(
    #         address_table.c.email_address.label('email'),
    #         (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
    #     )
    #         .where(
    #             user_table.c.id > 1
    #         )
    #         .join_from(user_table, address_table)
    # )
    # print(result.all())
    '''
    #     2025-11-13 13:59:59,042 INFO sqlalchemy.engine.Engine SELECT addresses.email_address AS email, users.first_name || ? || users.first_name AS full_name 
    #     FROM users JOIN addresses ON users.id = addresses.user_id 
    #     WHERE users.id > ?
    #     2025-11-13 13:59:59,042 INFO sqlalchemy.engine.Engine [generated in 0.00004s] (' ', 1)
    #     [('test2@yandex.ru', 'Test2 Test2'), ('test3@yandex.ru', 'Test3 Test3'), ('test4@yandex.ru', 'Test4 Test4')]
    '''
    # автоматический создались блоки ON

    # ------------------------------------------------------------
    # --- SELECT из разных таблиц (ручное указание ON)
    # ------------------------------------------------------------

    # result = conn.execute(
    #     select(
    #         address_table.c.email_address.label('email'),
    #         (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
    #     )
    #         .where(
    #             user_table.c.id > 1
    #         )
    #         .join_from(user_table, address_table, onclause=and_(user_table.c.id == address_table.c.user_id))
    # )
    # print(result.all())

    # ------------------------------------------------------------
    # --- SELECT из разных таблиц (просто join, без join_from)
    # ------------------------------------------------------------
    #
    # result = conn.execute(
    #     select(
    #         address_table.c.email_address.label('email'),
    #         (user_table.c.first_name + ' ' + user_table.c.first_name).label('full_name')
    #     )
    #     .where(
    #         user_table.c.id > 1
    #     )
    #     .join(address_table)
    #     .order_by(
    #         desc('full_name')  # можно обращаться по созданному лейблу
    #         # desc(user_table.c.first_name)  # (user_table.c.first_name).desc() то же самое
    #     )
    #     # .group_by(...)
    #     # .having(...)
    #     # .limit(10)
    # )
    # print(result.all())
    # здесь всё происходит полностью автоматически. Даже не нужно указывать левую сторону.
    # также есть различные методы left, outer, right
    # .join(address_table, isouter=True)
    # .join(address_table, full=True)
    # full left


# ------------------------------------------------------------
# --- UPDATE
# ------------------------------------------------------------

# with engine.begin() as conn: # type: Connection
    # UPDATE table SET name=1, fullname=2 WHERE

    # # FixMe Обычный режим
    # conn.execute(
    #     update(user_table)
    #     .where(user_table.c.id == 1)
    #     .values(first_name='Test111', second_name='Test111_second_name')
    # )
    # print(
    #     conn.execute(
    #         select(user_table).where(user_table.c.id == 1)
    #     ).all()
    # )

    # # FixMe bulk режим
    # # bindparam <----  Задаем переменную
    # stmt = (
    #     update(user_table)
    #         .where(user_table.c.first_name == bindparam('old_name'))
    #         .values(first_name=bindparam('new_name'))
    # )
    # conn.execute(
    #     stmt,
    #     parameters=[
    #         {'old_name': 'Test1', 'new_name': 'Test1_updated'},
    #         {'old_name': 'Test2', 'new_name': 'Test2_updated'},
    #         {'old_name': 'Test3', 'new_name': 'Test3_updated'},
    #     ]
    # )
    # print(conn.execute(select(user_table)).all())


# ------------------------------------------------------------
# --- DELETE
# ------------------------------------------------------------

# with engine.begin() as conn: # type: Connection
#     delete_stmt = delete(user_table).where(user_table.c.id == 1)
#     result = conn.execute(
#         delete_stmt
#     )
#     print(" --------- > Deleted", result.rowcount)
#     print(conn.execute(select(user_table)).all())

# ------------------------------------------------------------
# --- DELETE - удаление значений из нескольких таблиц
# ------------------------------------------------------------

# with engine.begin() as conn: # type: Connection
#     delete_stmt = (
#         delete(user_table)
#             .where(user_table.c.id == address_table.c.user_id)
#             .where(address_table.c.email_address == 'test1@yandex.ru')
#     )
#     # conn.execute(
#     #     delete_stmt
#     # )
#     conn.execute(delete_stmt)
#     print('-' * 100)
#     print(delete_stmt.compile(dialect=postgresql.dialect()))
#     print('-' * 100)


# ------------------------------------------------------------
# --- returning - (есть во всех конструкциях кроме SELECT)
# ------------------------------------------------------------

with engine.begin() as conn: # type: Connection
    conn.execute(
        delete(
            user_table,
        )
            .where(user_table.c.id == 1)
            .returning(user_table.c.id)

    )
    result = conn.execute(select(user_table)).all()
    print(result)