# создание обращения к базе данных
from sqlalchemy import create_engine, text



# диалект + драйвер :// /: база данных - в данном случае memory - оперативка компа
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

# соединение создается только тогда, когда это реально нужно

# открываем соединение
# with engine.connect() as connection:
#     query = text("select 'hello world!'")
#     result = connection.execute(query)
#     print(result)


# (sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % uv run -m lesson_2.lesson_1
# 2025-11-12 15:03:55,407 INFO sqlalchemy.engine.Engine BEGIN (implicit) # FixMe <-- начало транзакции
# 2025-11-12 15:03:55,407 INFO sqlalchemy.engine.Engine select 'hello world!'
# 2025-11-12 15:03:55,407 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
# <sqlalchemy.engine.cursor.CursorResult object at 0x107a94130> # FixMe <----------- результат
# 2025-11-12 15:03:55,407 INFO sqlalchemy.engine.Engine ROLLBACK # FixMe <---------- конец транзакции


# with engine.connect() as connection:
#     query = text("select 'hello world!'")
#     result = connection.execute(query)
#     print(result.scalars().all()) # all

# (sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % uv run -m lesson_2.lesson_1
# 2025-11-12 15:07:05,779 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2025-11-12 15:07:05,779 INFO sqlalchemy.engine.Engine select 'hello world!'
# 2025-11-12 15:07:05,779 INFO sqlalchemy.engine.Engine [generated in 0.00010s] ()
# [('hello world!',)]
# 2025-11-12 15:07:05,779 INFO sqlalchemy.engine.Engine ROLLBACK

# есть:
# all() - выводит [('hello world!',)]
# scalar() - выводит сразу строку - hello world!
# можно комбинировать result.scalars().all() - ['hello world!']
# scalar_one() - строго 1 результат или выбрасывает исключение
# scalar_one_or_none - возвращает либо 1 результат либо None, если количество результатов отличается от одного


with engine.connect() as connection:
    query = text("select 'hello world!'")
    result = connection.execute(query)
    print(result.scalars().one_or_none()) # all
    print(result.scalar_one_or_none())  # all


# В данном случае соединение закрыто:

# (sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % uv run -m lesson_2.lesson_1
# 2025-11-12 15:13:59,010 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2025-11-12 15:13:59,010 INFO sqlalchemy.engine.Engine select 'hello world!'
# 2025-11-12 15:13:59,010 INFO sqlalchemy.engine.Engine [generated in 0.00009s] ()
# hello world!
# 2025-11-12 15:13:59,010 INFO sqlalchemy.engine.Engine ROLLBACK
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/lesson_2/lesson_10_01.py", line 50, in <module>
#     print(result.scalar_one_or_none())  # all
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/.venv/lib/python3.11/site-packages/sqlalchemy/engine/result.py", line 1492, in scalar_one_or_none
#     return self._only_one_row(
#            ^^^^^^^^^^^^^^^^^^^
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/.venv/lib/python3.11/site-packages/sqlalchemy/engine/result.py", line 757, in _only_one_row
#     row: Optional[_InterimRowType[Any]] = onerow(hard_close=True)
#                                           ^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/.venv/lib/python3.11/site-packages/sqlalchemy/engine/cursor.py", line 2132, in _fetchone_impl
#     return self.cursor_strategy.fetchone(self, self.cursor, hard_close)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/.venv/lib/python3.11/site-packages/sqlalchemy/engine/cursor.py", line 1000, in fetchone
#     return self._non_result(result, None)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/.venv/lib/python3.11/site-packages/sqlalchemy/engine/cursor.py", line 1027, in _non_result
#     raise exc.ResourceClosedError(
# sqlalchemy.exc.ResourceClosedError: This result object is closed.


# чтобы пройтись по всем, нужно, например, сделать генератор:
# with engine.connect() as connection:
#     query = text("select 'hello world!'")
#     result = connection.execute(query)
#     for entry in result.scalars():
#         ...