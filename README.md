# max-bot-template

Шаблон бота для MAX на Python (maxapi) с PostgreSQL. В комплекте — стартовые
хендлеры `/start` и `/help`, модели пользователей и диалогов, а также базовая
структура проекта.

## Возможности

- Long polling через `maxapi.Dispatcher`
- Хранение пользователей и диалогов в PostgreSQL (SQLAlchemy 2.x)
- Автоматическое создание таблиц при старте (опционально)
- Миграции схемы через Alembic
- Конфигурация через `.env`

## Требования

- Python 3.12+
- PostgreSQL 16+
- `uv` для управления окружением и зависимостями

## Быстрый старт

1. Скопируйте `.env.example` в `.env` и заполните значения.
2. Подготовьте базу данных PostgreSQL.
3. Установите зависимости и запустите бота:

```bash
uv venv
uv sync
source .venv/bin/activate
python src/main.py
```

Полная инструкция: `docs/quick-start.md`.

## Миграции (Alembic)

Alembic берёт параметры подключения из `.env`, поэтому `alembic.ini` править не нужно.

1. Примените миграции из репозитория:

```bash
alembic upgrade head
```

2. При изменениях моделей создайте новую миграцию и примените:

```bash
alembic revision --autogenerate -m "add_field"
alembic upgrade head
```

## Переменные окружения

| Переменная | Описание |
| --- | --- |
| `MAX_BOT_TOKEN` | Токен бота в MAX |
| `MAX_BOT_USERNAME` | Username бота |
| `DB_USER` | Пользователь БД |
| `DB_PASS` | Пароль пользователя БД |
| `DB_NAME` | Имя базы |
| `DB_HOST` | Хост БД (по умолчанию `localhost`) |
| `DB_PORT` | Порт БД (по умолчанию `5432`) |
| `DB_AUTO_CREATE` | Автосоздание таблиц при старте (`1`/`0`, по умолчанию `1`) |

## Структура проекта

- `src/main.py` — точка входа, запуск polling.
- `src/handlers/` — обработчики `/start` и `/help`.
- `src/db/` — модели, DAO, подключение к БД.
- `src/config.py` — загрузка переменных окружения.
- `alembic/` — миграции и настройка окружения Alembic.
- `alembic.ini` — конфигурация Alembic (URL берётся из `.env`).
- `docs/` — гайды и справка по maxapi.

## Как расширять

- Добавляйте обработчики в `src/handlers/` и регистрируйте в
  `src/handlers/__init__.py`.
- Добавляйте модели в `src/db/models.py` и работайте с ними через DAO.

## Важно

- Для long polling у бота не должно быть активного webhook.
- Для создания бота в MAX нужен подтвержденный аккаунт юр. лица.
