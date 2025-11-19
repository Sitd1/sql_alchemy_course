# SQLAlchemy Курс 2

Этот проект представляет собой практику из курса по изучению SQLAlchemy 2.x с использованием инструментов для работы с базами данных.

Сам видеокурс:
https://youtu.be/leeC0fpAY-E

## 🚀 Технологии

- **SQLAlchemy 2.x** - ORM для работы с базами данных
- **PostgreSQL** - реляционная база данных
- **Alembic** - инструмент для миграций базы данных
- **asyncpg** - асинхронный драйвер PostgreSQL
- **Docker** - контейнеризация базы данных
- **uv** - менеджер зависимостей

## 📁 Структура проекта

```
sql_alchemy_course_2/
├── lesson_02/           # Основы работы с SQLAlchemy
├── lesson_03/           # Продвинутые запросы
├── lesson_04/           # Работа с данными
├── lesson_05_06/        # Комплексные запросы
├── lesson_08_orm/       # Введение в ORM
├── lesson_09_relations/ # Отношения между таблицами
│   ├── lesson_9_1_one_to_one.py     # Один к одному
│   ├── lesson_9_2_many_to_one.py    # Многие к одному
│   ├── lesson_9_3_many_to_many.py   # Многие ко многим
│   └── lesson_9_4_loads.py          # Загрузка связанных данных
└── lesson_10_alembic/   # Работа с миграциями Alembic
```

## 🛠 Установка и настройка

### 1. Клонирование репозитория

```bash
git clone git@github.com:Sitd1/sql_alchemy_course.git
cd sql_alchemy_course_2
```

### 2. Установка зависимостей

```bash
uv sync
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
cp .env.example .env
```

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=sql_lessons
DB_HOST=localhost
```

### 4. Запуск PostgreSQL через Docker

```bash
docker-compose up -d
```

### 5. Проверка установки

```bash
uv run python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"
```

## 📚 Уроки

### Урок 2: Основы работы с SQLAlchemy
- Создание соединения с базой данных
- Выполнение простых запросов
- Работа с результатами запросов

### Урок 3: Продвинутые запросы
- Сложные SQL-запросы
- Фильтрация и сортировка данных

### Урок 4: Манипуляция данными
- INSERT, UPDATE, DELETE операции
- Транзакции

### Урок 5-6: Комплексные запросы
- JOIN операции
- Агрегатные функции
- Подзапросы

### Урок 8: ORM (Object-Relational Mapping)
- Определение моделей
- Создание таблиц через ORM
- Базовые CRUD операции

### Урок 9: Отношения между таблицами
- **9.1**: Отношения "один к одному"
- **9.2**: Отношения "многие к одному"
- **9.3**: Отношения "многие ко многим"
- **9.4**: Стратегии загрузки связанных данных

### Урок 10: Миграции с Alembic
- Настройка Alembic
- Создание и применение миграций
- Откат миграций
- Автоматическая генерация миграций

## 🏃‍♂️ Запуск уроков

Каждый урок можно запустить отдельно:

```bash
# Урок 2
uv run -m lesson_02.lesson_1

# Урок 3
uv run -m lesson_03.lesson_3

# Урок по Alembic
uv run -m lesson_10_alembic.lesson_10_01
```

## 🔧 Основные команды Alembic

```bash
# Инициализация миграций
alembic init migrations

# Создание новой миграции
alembic revision -m "description" --autogenerate

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Просмотр текущего статуса
alembic current
```

## 📖 Дополнительные материалы

- [Официальная документация SQLAlchemy](https://sqlalchemy.org/)
- [Документация FastAPI](https://fastapi.tiangolo.com/)
- [Руководство по Alembic](https://alembic.sqlalchemy.org/)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request


## 📞 Контакты

Если у вас возникли вопросы или предложения, создайте issue в репозитории проекта.
tg: @sitd1
