# План миграции REST API из functions/ в backend_project/

## Статус: В процессе

### ✅ Завершено (v0.0.1)
- [x] Email аутентификация (signup/login/logout)
- [x] JWT токены (access + refresh)
- [x] Redis blacklist для logout
- [x] Swagger/OpenAPI документация
- [x] Django admin
- [x] Тесты для authentication endpoints
- [x] Конфигурация через .env
- [x] CI/CD (GitHub Actions)

### 🔄 В процессе
- [ ] Синхронизация модели User (functions/ → backend_project/)
- [ ] Миграция AuthService (bcrypt hashing)

### 📋 Очередь миграции

#### 1. Phone Authentication
**Файлы для переноса:**
- `functions/auth.py` → `backend_project/api/views/phone_auth_views.py`
- `functions/models/user.py` → обновить `backend_project/api/models.py`
- `functions/services/auth_service.py` → `backend_project/api/services/auth_service.py`

**Endpoints:**
- `POST /auth/phone` - отправка SMS кода
- `POST /auth/phone/verify` - проверка SMS кода

**Зависимости:**
- SMS шлюз (требуется интеграция)
- Redis для хранения SMS кодов

**Приоритет:** Средний

---

#### 2. Telegram Authentication
**Файлы для переноса:**
- `functions/auth.py` → `backend_project/api/views/telegram_auth_views.py`
- `functions/handlers.py` → `backend_project/api/telegram/` (новая директория)

**Endpoints:**
- `POST /auth/telegram` - проверка Telegram данных

**Зависимости:**
- Telegram Bot API
- Firebase Functions (возможно)

**Приоритет:** Высокий (основной метод аутентификации)

---

#### 3. Refresh Token Endpoint
**Файлы для переноса:**
- `functions/auth.py` → `backend_project/api/views/jwt_views.py`

**Endpoints:**
- `POST /auth/refresh` - обновление JWT токена

**Зависимости:**
- JWT utilities (уже есть в backend_project/)

**Приоритет:** Высокий

---

#### 4. User Profile Management
**Файлы для переноса:**
- `functions/auth.py` (UserResponseSchema) → `backend_project/api/serializers.py`

**Endpoints:**
- `GET /auth/me` - текущий пользователь (✅ уже есть)
- `PUT /auth/me` - обновление профиля
- `DELETE /auth/me` - удаление аккаунта

**Приоритет:** Средний

---

#### 5. Provider Authentication
**Файлы для переноса:**
- `functions/` (provider endpoints)

**Endpoints:**
- `POST /auth/provider` - аутентификация провайдера
- `GET /provider/dashboard` - панель провайдера

**Зависимости:**
- Provider модель (требуется создать)

**Приоритет:** Низкий

---

## Технические задачи

### База данных
- [ ] Сравнить модели User в functions/ и backend_project/
- [ ] Создать миграцию для добавления `password_hash` поля
- [ ] Добавить индексы для phone и telegram_id

### Безопасность
- [ ] Настроить rate limiting для auth endpoints
- [ ] Добавить валидацию паролей (требования к сложности)
- [ ] Настроить HTTPS для production

### Тестирование
- [ ] Добавить тесты для phone auth
- [ ] Добавить тесты для telegram auth
- [ ] Добавить интеграционные тесты
- [ ] Настроить code coverage reporting

### Документация
- [ ] Обновить Swagger документацию
- [ ] Добавить примеры запросов/ответов
- [ ] Создать API changelog

---

## Хронология миграции

### Этап 1: Базовая функциональность (v0.0.1) ✅
- Email аутентификация
- JWT токены
- Swagger документация
- Тесты

### Этап 2: Критичные функции (v0.0.2)
- Refresh token endpoint
- Telegram аутентификация
- Синхронизация модели User

### Этап 3: Дополнительные функции (v0.0.3)
- Phone аутентификация
- User profile management
- Rate limiting

### Этап 4: Production готовность (v0.1.0)
- Provider authentication
- Полное тестирование
- Production настройки
- Мониторинг и логирование

---

## Контакты и ресурсы

**Репозитории:**
- functions/ (FastAPI) - текущее API
- backend_project/ (Django) - новое API

**Документация:**
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg (Swagger)](https://drf-yasg.readthedocs.io/)
- [Firebase Functions](https://firebase.google.com/docs/functions)

**Команда:**
- Backend разработчик: @RedAlexDad
- Code reviewer: TBD
