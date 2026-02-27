# Настройка окружения

## Быстрый старт

1. Скопируйте `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```

2. При необходимости измените переменные в `.env`

3. Запустите проект:
   ```bash
   make up
   ```

## Переменные окружения

### Django
- `DEBUG` - режим отладки (True/False)
- `SECRET_KEY` - секретный ключ Django
- `ALLOWED_HOSTS` - разрешенные хосты

### База данных (PostgreSQL)
- `DB_ENGINE` - движок БД (по умолчанию: django.db.backends.postgresql)
- `DB_NAME` - имя базы данных
- `DB_USER` - пользователь БД
- `DB_PASSWORD` - пароль БД
- `DB_HOST` - хост БД
- `DB_PORT` - порт БД

### JWT
- `JWT_SECRET` - секретный ключ для JWT
- `JWT_ALGORITHM` - алгоритм JWT (по умолчанию: HS256)
- `JWT_EXPIRATION_HOURS` - время жизни токена в часах

### CORS
- `ALLOWED_ORIGINS` - разрешенные CORS origin (через запятую)

### CSRF
- `CSRF_TRUSTED_ORIGINS` - доверенные CSRF origin (через запятую)
- `CSRF_COOKIE_HTTPONLY` - HttpOnly флаг для CSRF cookie
- `CSRF_COOKIE_SAMESITE` - SameSite атрибут (Lax/Strict/None)
- `CSRF_COOKIE_SECURE` - Secure флаг для CSRF cookie

### Redis
- `REDIS_HOST` - хост Redis
- `REDIS_PORT` - порт Redis
- `REDIS_DB` - номер базы данных Redis
- `REDIS_PASSWORD` - пароль Redis

## Безопасность

⚠️ **Никогда не коммитьте `.env` в git!**

Файл `.env` добавлен в `.gitignore` и не должен попадать в репозиторий.
Используйте `.env.example` как шаблон для документации.

## Production

Для production окружения:
1. Установите `DEBUG=False`
2. Сгенерируйте новый `SECRET_KEY`
3. Установите `CSRF_COOKIE_SECURE=True`
4. Настройте `ALLOWED_ORIGINS` и `CSRF_TRUSTED_ORIGINS` для вашего домена
