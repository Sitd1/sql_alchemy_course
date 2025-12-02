```bash
  uv run alembic init migrations
```

1. Проверили `alembic.ini`
2. Поправили `migrations/env.py`
   1. ```angular2html
    config.set_main_option(
        'sqlalchemy.url',
        config_settings.db.url_psycopg # переопределили
    )
    ```
   
   2. target_metadata = Base.metadata

3. Создаем версию миграции
```bash
  alembic revision -m 'init' --autogenerate
```

4. Примененяем миграции к БД
```bash
  alembic upgrade head
```
