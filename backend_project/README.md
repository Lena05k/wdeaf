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

```
backend_project/
├── backend/              # Настройки Django проекта
├── api/                  # Основное API приложение
│   ├── models/           # Модели данных
│   │   └── user.py       # User модель (AbstractBaseUser)
│   │
│   ├── serializers/      # DRF сериализаторы
│   │   ├── auth.py       # Аутентификация (login/signup)
│   │   ├── user.py       # Пользователь (UserSerializer)
│   │   ├── provider.py   # Провайдеры услуг
│   │   ├── telegram.py   # Telegram auth
│   │   └── phone.py      # Phone auth
│   │
│   ├── services/         # Бизнес-логика
│   │   ├── auth/         # Сервисы аутентификации
│   │   │   ├── email_auth.py      # EmailAuthService
│   │   │   ├── telegram_auth.py   # TelegramAuthService
│   │   │   ├── phone_auth.py      # PhoneAuthService
│   │   │   └── provider_auth.py   # ProviderAuthService
│   │   └── token/        # Токен сервисы
│   │       ├── jwt_service.py       # JWTService
│   │       └── blacklist_service.py # TokenBlacklistService
│   │
│   ├── repositories/     # Слой доступа к данным
│   │   └── user_repo.py  # UserRepository
│   │
│   ├── utils/            # Утилиты
│   │   ├── responses.py  # AuthResponseBuilder (DRY)
│   │   └── validators.py # Валидаторы
│   │
│   ├── views/            # API Views
│   │   ├── auth_views.py        # Login/Signup/Logout
│   │   ├── user_profile_views.py # Profile update/delete
│   │   ├── provider_views.py     # Provider endpoints
│   │   ├── telegram_auth_views.py # Telegram auth
│   │   └── phone_auth_views.py    # Phone auth
│   │
│   ├── tests/            # Тесты
│   │   ├── test_auth.py         # Auth тесты (10)
│   │   ├── test_user_profile.py # Profile тесты (4)
│   │   └── test_provider.py     # Provider тесты (3)
│   │
│   ├── authentication.py # JWT аутентификация с CSRF
│   └── urls.py           # URL маршруты
│
├── manage.py             # Django утилита
├── requirements.txt      # Зависимости
├── .env.example          # Пример переменных окружения
└── Makefile              # Команды для разработки
```

## Модульная архитектура

Проект использует **модульную архитектуру** с разделением ответственности:

### Архитектурные паттерны

#### 1. Repository Pattern (Репозиторий)
**Где:** `api/repositories/user_repo.py`

```python
class UserRepository:
    def get_by_email(self, email): ...
    def create_user(self, email, password, ...): ...
    def update(self, user, **kwargs): ...
```

**Зачем:**
- ✅ Изолирует доступ к базе данных
- ✅ Легко тестировать (можно замокать)
- ✅ Можно сменить ORM/БД без изменения бизнес-логики

#### 2. Service Layer Pattern (Сервисный слой)
**Где:** `api/services/auth/*.py`, `api/services/token/*.py`

```python
class EmailAuthService:
    def __init__(self):
        self.user_repo = UserRepository()  # ← Dependency Injection
    
    def register(self, email, password, ...):
        # Бизнес-логика
    
    def authenticate(self, email, password):
        # Бизнес-логика
```

**Зачем:**
- ✅ Бизнес-логика отдельно от HTTP слоя
- ✅ Single Responsibility Principle
- ✅ Переиспользование логики между разными views

#### 3. Dependency Injection (Внедрение зависимостей)
**Где:** Конструкторы сервисов

```python
class EmailAuthService:
    def __init__(self):
        self.user_repo = UserRepository()  # ← Внедрение зависимости
```

**Зачем:**
- ✅ Легко заменять реализации (например, для тестов)
- ✅ Слабая связанность компонентов
- ✅ Проще тестировать

#### 4. Builder Pattern (Строитель)
**Где:** `api/utils/responses.py`

```python
class AuthResponseBuilder:
    @staticmethod
    def with_jwt(user, status_code=200):
        # Строит ответ с JWT токенами
    
    @staticmethod
    def success(data, message):
        # Строит успешный ответ
```

**Зачем:**
- ✅ DRY - нет дублирования кода
- ✅ Консистентность ответов API
- ✅ Централизованное управление форматом ответов

#### 5. Layered Architecture (Многослойная архитектура)

```
┌─────────────────────────────────────┐
│         HTTP Layer (Views)          │  ← API Views
├─────────────────────────────────────┤
│       Service Layer (Services)      │  ← Бизнес-логика
├─────────────────────────────────────┤
│    Repository Layer (Repositories)  │  ← Доступ к данным
├─────────────────────────────────────┤
│         Database (PostgreSQL)       │  ← БД
└─────────────────────────────────────┘
```

**Поток запроса:**
```
HTTP Request → View → Service → Repository → Database
HTTP Response ← View ← Service ← Repository ← Database
```

#### 6. DTO Pattern (Data Transfer Object)
**Где:** `api/serializers/*.py`

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', ...]
```

**Зачем:**
- ✅ Преобразование между DB и API форматами
- ✅ Валидация данных
- ✅ Сериализация/десериализация

---

### 1. Models (Модели)
```python
# api/models/user.py
class User(AbstractBaseUser):
    # Кастомная модель пользователя
    # AbstractBaseUser + UserManager
```

### 2. Repositories (Репозитории)
Изолируют доступ к базе данных:
```python
# api/repositories/user_repo.py
class UserRepository:
    def get_by_email(self, email): ...
    def create_user(self, email, password, ...): ...
    def update(self, user, **kwargs): ...
```

**Преимущества:**
- ✅ Легко тестировать (можно замокать)
- ✅ Можно сменить БД без изменения сервисов
- ✅ Вся логика доступа к данным в одном месте

### 3. Services (Сервисы)
Бизнес-логика приложения:
```python
# api/services/auth/email_auth.py
class EmailAuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register(self, email, password, ...):
        # Бизнес-логика регистрации
    
    def authenticate(self, email, password):
        # Бизнес-логика аутентификации
```

**Принципы:**
- ✅ Single Responsibility Principle
- ✅ Dependency Injection (через repository)
- ✅ Нет прямого доступа к ORM в views

### 4. Utils (Утилиты)
Общие вспомогательные классы:
```python
# api/utils/responses.py
class AuthResponseBuilder:
    @staticmethod
    def with_jwt(user, status_code=200):
        # DRY - создание ответа с JWT токенами
```

### 5. Views (Представления)
Тонкий слой между HTTP и сервисами:
```python
# api/views/auth_views.py
class LoginView(APIView):
    def post(self, request):
        auth_service = EmailAuthService()
        user = auth_service.authenticate(...)
        return AuthResponseBuilder.with_jwt(user)
```

## Примеры использования

### Регистрация пользователя
```python
from api.services.auth import EmailAuthService
from api.utils.responses import AuthResponseBuilder

# В view
auth_service = EmailAuthService()
user = auth_service.register(
    email='user@example.com',
    password='securepass123',
    first_name='John'
)
return AuthResponseBuilder.with_jwt(user)
```

### Аутентификация провайдера
```python
from api.services.auth import ProviderAuthService

provider_service = ProviderAuthService()
provider = provider_service.register(
    email='provider@company.com',
    password='secretpass123',
    first_name='Company',
    phone='+77771234567'
)
```

### Работа с токенами
```python
from api.services.token import JWTService, TokenBlacklistService

jwt_service = JWTService()
access_token = jwt_service.create_access_token(user_id)
refresh_token = jwt_service.create_refresh_token(user_id)

# Blacklist при logout
blacklist_service = TokenBlacklistService()
blacklist_service.add_to_blacklist(token, expires_at)
```

## Запуск тестов

```bash
# Все тесты
python manage.py test api.tests

# Конкретный модуль
python manage.py test api.tests.test_auth
python manage.py test api.tests.test_provider

# Через Makefile
make test           # Запуск тестов
make test-verbose   # С подробным выводом
```

## API Endpoints

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/auth/signup` | POST | Регистрация |
| `/auth/login` | POST | Вход |
| `/auth/logout` | POST | Выход |
| `/auth/me` | GET | Текущий пользователь |
| `/auth/me/update` | PUT/PATCH | Обновление профиля |
| `/auth/me/delete` | DELETE | Удаление аккаунта |
| `/auth/refresh` | POST | Обновление токена |
| `/auth/telegram` | POST | Telegram auth |
| `/auth/phone` | POST | Phone auth |
| `/provider/signup` | POST | Регистрация провайдера |
| `/provider/list` | GET | Список провайдеров |
| `/health` | GET | Health check |
| `/swagger/` | GET | Swagger документация |

## Миграция с Functions

Смотри подробный чек-лист миграции в файле `MIGRATION_CHECKLIST.md`

## Документация

- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/
- **OpenAPI JSON:** http://localhost:8000/api/swagger.json