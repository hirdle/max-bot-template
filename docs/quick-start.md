# Гайд по началу работы с max-bot-template

Все команды выполняйте из корня
проекта, чтобы `.env` был корректно подхвачен.

## Требования

- Python 3.12+
- PostgreSQL 16+
- `uv` для управления окружением и зависимостями

## 1. Подготовка переменных окружения

Скопируйте пример и заполните значения:

```bash
cp .env.example .env
```

В `.env` укажите:

- `MAX_BOT_TOKEN` — токен бота в MAX.
- `MAX_BOT_USERNAME` — username бота (как в кабинете MAX).
- `DB_USER`, `DB_PASS`, `DB_NAME` — параметры подключения к БД.
- `DB_HOST`, `DB_PORT` — опционально (по умолчанию `localhost:5432`).

## 2. Инициализация базы данных

Используется PostgreSQL. Создайте пользователя и базу:

```sql
CREATE DATABASE <DB_NAME> WITH ENCODING='UTF-8';
CREATE USER <DB_USER> WITH PASSWORD '<DB_PASS>';
ALTER ROLE <DB_USER> SET client_encoding TO 'utf8';
ALTER ROLE <DB_USER> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <DB_USER> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <DB_USER>;
```

По умолчанию таблицы создаются автоматически при старте приложения
(`src/db/database.py:init_db`). Если хотите работать через миграции Alembic,
установите `DB_AUTO_CREATE=0` в `.env` (миграции применяются отдельным шагом).

## 3. Установка зависимостей

```bash
uv venv
uv sync
source .venv/bin/activate
```

## 4. Миграции (Alembic)

Если оставляете `DB_AUTO_CREATE=1`, этот шаг можно пропустить.

Alembic использует те же переменные подключения из `.env`, поэтому `alembic.ini`
править не нужно.

Примените миграции из репозитория:

```bash
alembic upgrade head
```

Если меняете модели, создайте новую миграцию и примените:

```bash
alembic revision --autogenerate -m "add_field"
alembic upgrade head
```

## 5. Запуск бота

```bash
python src/main.py
```

## Что дальше

- Хендлеры лежат в `src/handlers/`, регистрация — в
  `src/handlers/__init__.py`.
- Модели и DAO — в `src/db/`.
- Конфигурация — в `src/config.py`.

## Возможные трудности

1. Для работы в режиме long polling у бота не должно быть активного webhook.
2. Для создания бота в MAX нужен подтвержденный аккаунт юр. лица.
3. На данный момент смена username для бота недоступна.
4. Если при старте получаете ошибку `Missing database settings`, проверьте
   заполнение `.env`.
