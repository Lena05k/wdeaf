# WDEAF - Django Backend + Vue 3 Frontend

## 📋 Обзор

Проект состоит из двух основных частей:
- **Backend**: Django REST API (`backend_project/`)
- **Frontend**: Vue 3 + Vite (`frontend/`)

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd wdeaf
```

### 2. Настройка окружения
```bash
# Скопируйте .env.example в .env
cp .env.example .env

# Отредактируйте .env при необходимости
# Минимальные настройки:
# - TELEGRAM_BOT_TOKEN (если нужен Telegram)
# - JWT_SECRET (для production)
```

### 3. Запуск проекта
```bash
# Запуск всех сервисов
make up

# Или через docker compose
docker compose up -d
```

### 4. Проверка
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/swagger/
- **Django Admin**: http://localhost:8000/admin/

## 📁 Структура проекта

```
wdeaf/
├── backend_project/        # Django Backend
│   ├── api/               # API приложение
│   │   ├── models/        # Модели
│   │   ├── serializers/   # Сериализаторы
│   │   ├── services/      # Бизнес-логика
│   │   ├── views/         # API Views
│   │   └── tests/         # Тесты
│   ├── backend/           # Настройки Django
│   └── manage.py          # Django CLI
│
├── frontend/              # Vue 3 Frontend
│   ├── src/
│   │   ├── components/    # Vue компоненты
│   │   ├── views/         # Страницы
│   │   └── api/           # API клиенты
│   └── package.json
│
├── docker-compose.yml     # Docker конфигурация
├── .env.example          # Пример окружения
├── .env                  # Локальное окружение (не в git)
└── Makefile              # Команды для разработки
```

## 🔧 Команды разработки

```bash
# Запуск всех сервисов
make up

# Запуск с авто-исправлением проблем БД (рекомендуется для нового окружения)
make up-safe

# Инициализация PostgreSQL (проверка пользователя, БД, пароля)
make init-db

# Остановка сервисов
make down

# Пересборка с авто-проверкой БД
make rebuild

# Пересборка без кэша с авто-проверкой БД
make rebuild-no-cache

# Просмотр логов
make logs
make logs-backend    # Только backend
make logs-frontend   # Только frontend

# Проверка подключения к БД
make check-db

# Сброс volumes (при проблемах с паролем/версией PostgreSQL)
make reset-volumes

# Тесты
make test

# Миграции БД
make migrate

# Сброс БД (внимание: удаляет все данные!)
make reset-db

# Shell в контейнерах
make shell-backend
make shell-frontend

# Полная очистка
make clean
```

## 🗄️ База данных

### PostgreSQL
- **Хост**: localhost:5432
- **База**: wdeaf
- **Пользователь**: postgres
- **Пароль**: postgres

### Redis
- **Хост**: localhost:6379
- **Пароль**: нет (для разработки)

## 🔐 Суперпользователь Django

После `make reset-db` создаётся суперпользователь:
- **Email**: admin@example.com
- **Пароль**: adminadmin

## 📊 API Документация

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI JSON**: http://localhost:8000/api/swagger.json

## 🧪 Тестирование

```bash
# Все тесты
make test

# Конкретный модуль
docker compose exec backend python manage.py test api.tests.test_auth
docker compose exec backend python manage.py test api.tests.test_provider

# С подробным выводом
docker compose exec backend python manage.py test api.tests --verbosity=2
```

## 🌐 Frontend API Client

Frontend использует `VITE_API_URL` для подключения к backend:

```javascript
// frontend/src/api/client.js
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Пример запроса
const response = await fetch(`${API_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})
```

## 🔒 Production настройки

### .env для production
```bash
# Security
JWT_SECRET=your-super-secret-production-key
SECRET_KEY=django-insecure-production-key-change-this

# Database
POSTGRES_PASSWORD=secure-production-password

# CORS
ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Cookies
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

### Docker Compose для production
```bash
# Используйте docker-compose.prod.yml
docker compose -f docker-compose.prod.yml up -d
```

## 🐛 Troubleshooting

### Ошибка аутентификации PostgreSQL

**Симптомы:**
```
django.db.utils.OperationalError: connection to server at "wdeaf-postgres" (172.18.0.2), port 5432 failed: FATAL:  password authentication failed for user "wdeaf_user"
```

**Причина:** Старый том Docker с другим паролем или измененные учетные данные в `.env`

**Решение (автоматическое):**
```bash
# Запуск с авто-исправлением проблем БД
make up-safe

# Или инициализация PostgreSQL
make init-db
```

**Решение (вручную):**
```bash
# Сброс volumes и пересоздание БД
make reset-volumes

# Или полная очистка
make clean
docker compose up -d
```

### Backend не запускается
```bash
# Проверьте логи
make logs-backend

# Пересоберите с проверкой БД
make rebuild
```

### Frontend не видит backend
```bash
# Проверьте VITE_API_URL в .env
# Должно быть: VITE_API_URL=http://localhost:8000

# Перезапустите frontend
docker compose restart frontend
```

### Ошибки миграции
```bash
# Сбросьте БД
make reset-db
```

### Конфликт версий PostgreSQL

**Симптомы:**
```
FATAL:  database files are incompatible with server
The data directory was initialized by PostgreSQL version 16, which is not compatible with this version 15.17
```

**Решение:**
```bash
# Сброс volumes
make reset-volumes
```

## 📚 Дополнительная документация

- [Backend README](backend_project/README.md)
- [API Documentation](http://localhost:8000/swagger/)
- [Django Docs](https://docs.djangoproject.com/)
- [Vue 3 Docs](https://vuejs.org/)

## 🔄 CI/CD

Проект использует GitHub Actions для автоматического тестирования и сборки.

### Workflow файлы

- **`.github/workflows/ci-cd.yml`** — основной CI/CD пайплайн

### Этапы CI/CD

#### 1. Backend Tests
- Установка Python 3.12
- Установка зависимостей
- Запуск PostgreSQL 15 и Redis 7
- Создание пользователя БД и предоставление прав
- Применение миграций
- Запуск тестов
- Проверка `collectstatic`

#### 2. Frontend Build
- Установка Node 20
- Установка зависимостей
- Линтинг (если настроен)
- Сборка проекта
- Сохранение артефактов

#### 3. Docker Build Test
- Сборка Docker образов backend и frontend
- Проверка запуска контейнеров
- Кэширование сборок через GitHub Actions

#### 4. Docker Compose Integration
- Развертывание полного стека сервисов
- Инициализация БД (пользователь, права)
- Проверка health-статусов сервисов
- Тестирование доступности API

#### 5. Code Quality
- Проверка Python кода (flake8)
- Проверка полноты `.env.example`

### Запуск локально

```bash
# Запустить тесты backend
docker compose exec backend python manage.py test api.tests

# Запустить сборку frontend
docker compose exec frontend npm run build

# Проверить Docker сборку
make rebuild-no-cache
```
