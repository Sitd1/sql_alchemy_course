# Основные команды
```bash
alembic revision -m "first" --autogenerate
alembic upgrade head
alembic downgrade -1
alembic upgrade head
alembic revision -m "add email" --autogenerate
alembic upgrade head

```




# BD schema
Схема указывает какие таблицы с какими столбцами и связями существуют.

![img.png](img.png)

---

Если мы работаем без ORM - то про схему нам говорит сама база данных. 
В случае sqlAlchemyORM мы кодом задаем схему БД.
В таком случае нам нужно обновлять бд по ходу разработки.

Нам нужно сопоставлять эти обновления приложение -> БД

#### Способы:
- Вручную
- Удалять/поднимать
- Миграции


---

## Миграции

**Миграции** - скрипты, которые приводят нашу БД в какое-то состояние (версию), которое мы хотим видеть  

Миграции можно писать вручную или использовть утилиты

![img_1.png](img_1.png)

**Утилиты** помогают обновлять изменения автоматически  

### Scheme-bases

Просто вносят изменения при помощи raw SQL (не привязывается к моделям)

### Model-based

У нас есть ORM, ORM генерирует скрипт на питоне, затем этот код переводится в SQL скрипт и уже выполняется на самом БД.

# Alembic

**Alembic** - родная для SQLAlchemy утилита миграции. У них один и тот же разработчик 


## 1. Начало


### Инициализация миграции
```bash
alembic init migrations
```

где `migrations` -  это папка, куда будут закидыаться миграции

```angular2html
(sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % alembic init migrations
  Creating directory /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations ...  done
  Creating directory /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/versions ...  done
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/script.py.mako ...  done
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/env.py ...  done
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/README ...  done
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/alembic.ini ...  done
  Please edit configuration/connection/logging settings in /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/alembic.ini before proceeding.
```

#### Смотрим что создалось:
![img_3.png](img_3.png)

##### Смотрим alembic.ini

Единственная строка, которая нас интересует:

```angular2html
sqlalchemy.url = driver://user:pass@localhost/dbname
```

Лучше этот url не указывать - там пароли и юзеры
Такие данные лучше хранить в .env и их доставать оттуда же

Для этого придется корректировать файл

`migrations/env.py`

##### Смотрим `migrations/env.py`

Это тот файл, который будет накатывать (исполнять) наши миграции

1. Находим в ней строку: 

```target_metadata = None```

2. Указываем там нашу Метадату 

```target_metadata = Base.metadata```

(Не забываем делать импорт Base)

3. находим ```config = context.config```
4. под ней добавляем строку 

```
config.set_main_option(
    'sqlalchemy.url',
     URL.create(
         database=os.getenv("DB_NAME"),
         host=os.getenv("DB_HOST"),
         ...
     )
)
```
Или из других переменных, если они уже созданы, напр в configs/settings.py

URL импортируется из:
``` from sqlalchemy.engine.url import URL```

Например:
```angular2html
from lesson_10_alembic.settings import DATABASE_URL

config.set_main_option(
    'sqlalchemy.url',
    DATABASE_URL  # переопределили
)
```

### 2. Генерация первой миграции

```bash
alembic revision -m 'first'
```

Миграция создалась, но еще не применилась

```angular2html
Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/versions/1d35db476da0_first.py ...  done
```

![img_2.png](img_2.png)

В папке versions появилась первая миграция

![img_4.png](img_4.png)


```angular2html
# revision identifiers, used by Alembic.
revision: str = '1d35db476da0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
```

- `revision` - uid миграции
- down_revision - uid предыдущей ревизии (куда мы будет откатываться)
- branch_labels - ветки как в гит (есть возможность, но их не используют)
- depends_on - списки uid ревизий, от которых зависит данная ревизия (в реальности мы его не трогаем)


Чтобы миграция сгенерировалась нужно еще указать флаг

Удаляем то, что создавалось ранее

```bash
alembic revision -m 'first' --autogenerate
```
![img_5.png](img_5.png)


```logs
(sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % alembic revision -m 'first' --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/versions/cd947f5d765d_first.py ...  done
```

ТОЛЬКО не забываем удалять предыдущие эксперименты и очистить таблицы из БД (первая миграция)

теперь alembic:
- залезает в БД
- смотрит какие таблицы там есть (схему)
- видит разницу с нашей моделью 
- теперь генерирует всё как нужно (upgrade, downgrade)

Одна миграция отвечает и за `upgrade` и за `downgrade`


!!! Любую миграцию нужно проверять вручную (могут быть ошибки)

Напоминание: Миграция еще не применена на БД:
но при этом создана таблица alembic_version,
где хранится информация о текущей миграции (версия)

Но самой таблицы users еще нет 
![img_7.png](img_7.png)


Применение миграции к БД
```bash
alembic upgrade head
```
где `head` - последняя версия
или можно указывать uid миграции, если нужно перейти на определенную


```logs
(sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % alembic revision -m 'first' --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
  Generating /Users/denis.sitdikov/PycharmProjects/sql_alchemy_course_2/migrations/versions/287016b5c4cb_first.py ...  done
(sql_alchemy_course_2) denis.sitdikov@MacBook-Pro-Denis-2 sql_alchemy_course_2 % alembic upgrade head                      
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 287016b5c4cb, first
```


### downgrade

```bash
alembic downgrade -1
```

здесь тегов нет, но можно указать на сколько миграций нам нужно откатиться  



# !!! Важно

Необходимо тестить

STAIRWAY_TEST

бывает такое, что alembic творит дичь
Также бывает, что если сделать upgrade - downgrade - результат не такой как был прежде  

Миграции на enum может не работать и их нужно писать вручную

Миграция данных - отдельная тема

 
