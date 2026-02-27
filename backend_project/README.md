# Django Backend

Это Django приложение, которое заменяет собой старую систему функций (functions/).
Предназначено для обеспечения API для фронтенд-приложения.

## Стек технологий

- Python 3.x
- Django 6.0+
- Django REST Framework
- PostgreSQL (или другая поддерживаемая БД)

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения в `.env` файле

3. Выполните миграции:
```bash
python manage.py migrate
```

4. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `backend/` - основные настройки Django проекта
- `api/` - основное приложение с API эндпоинтами
- `manage.py` - утилита управления Django

## Миграция с Functions

Смотри подробный чек-лист миграции в файле `MIGRATION_CHECKLIST.md`