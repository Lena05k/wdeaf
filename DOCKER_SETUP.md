# WDEAF Docker Setup Guide

## 🎯 Автоматическая установка зависимостей

Теперь Docker **автоматически устанавливает** новые пакеты при изменении `package.json` или `requirements.txt`!

### Как это работает:

#### Frontend (npm)
```bash
# 1. Установи пакет локально
cd frontend
npm install -D sass-embedded

# 2. Просто перезагрузи контейнер
docker-compose restart wdeaf-frontend

# Готово! ✅ Новый пакет установлен автоматически
```

#### Backend (pip)
```bash
# 1. Добавь в requirements.txt
echo "new-package==1.0.0" >> functions/requirements.txt

# 2. Перезагрузи контейнер
docker-compose restart wdeaf-functions

# Готово! ✅ Новый пакет установлен автоматически
```

---

## 🚀 Быстрый старт

```bash
# Первый запуск
docker-compose up --build

# Обычный запуск
docker-compose up

# Остановка
docker-compose down

# Полная очистка (volumes)
docker-compose down -v
```

---

## 📦 Структура проекта

```
WDEAF_APP/
├── frontend/
│   ├── Dockerfile              # Frontend образ с npm
│   ├── docker-entrypoint.sh   # Автоустановка npm пакетов
│   ├── package.json
│   └── src/
├── functions/
│   ├── Dockerfile              # Backend образ с Python
│   ├── docker-entrypoint.sh   # Автоустановка pip пакетов
│   ├── requirements.txt
│   └── *.py
├── compose.yml                 # Production конфиг
├── compose.override.yml        # Development overrides
└── .env                        # Environment variables
```

---

## ⚙️ Environment Variables

Основные переменные в `.env`:

```bash
# Порты
DOCKER_FRONTEND_PORT=5173
DOCKER_FUNCTIONS_PORT=8000
DOCKER_POSTGRES_PORT=5432
DOCKER_REDIS_PORT=6379

# Database
DB_NAME=wdeaf_db
DB_USER=wdeaf_user
DB_PASSWORD=your_password_here

# Redis
REDIS_PASSWORD=your_redis_password

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
```

---

## 🔧 Полезные команды

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Только frontend
docker-compose logs -f wdeaf-frontend

# Только functions
docker-compose logs -f wdeaf-functions
```

### Вход в контейнер
```bash
# Frontend
docker exec -it wdeaf-frontend sh

# Functions
docker exec -it wdeaf-functions bash
```

### Ручная установка пакетов (если нужно)
```bash
# Frontend
docker exec -it wdeaf-frontend npm install package-name

# Functions
docker exec -it wdeaf-functions pip install package-name
```

### Пересборка одного сервиса
```bash
# Только frontend
docker-compose up --build wdeaf-frontend

# Только functions
docker-compose up --build wdeaf-functions
```

---

## 🐛 Troubleshooting

### Порт занят
```bash
Error: port is already allocated

# Решение:
docker-compose down
lsof -ti:5173 | xargs kill -9  # Убить процесс на порту
docker-compose up
```

### Контейнер не видит изменений
```bash
# Перезапуск с пересборкой
docker-compose up --build

# Или полная очистка
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Зависимости не установились
```bash
# Проверь что entrypoint скрипт выполнился
docker-compose logs wdeaf-frontend | grep "Installing"

# Если нет, пересобери образ
docker-compose build --no-cache wdeaf-frontend
docker-compose up
```

---

## 🎨 Hot Reload работает!

✅ **Frontend**: Vite hot-reload через volumes  
✅ **Backend**: Uvicorn `--reload` для Python  
✅ **Зависимости**: Автоматическая установка при restart  

---

## 📝 Workflow для разработки

1. **Запусти Docker один раз**
   ```bash
   docker-compose up
   ```

2. **Редактируй код** — изменения применяются мгновенно (hot-reload)

3. **Добавил новый пакет?**
   ```bash
   npm install new-package
   docker-compose restart wdeaf-frontend
   ```

4. **Всё работает!** 🚀

---

## 🔗 Доступ к сервисам

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## 💡 Преимущества текущей настройки

| Фича | Статус |
|------|--------|
| Hot reload (код) | ✅ Работает |
| Auto-install (пакеты) | ✅ Работает |
| Volumes для кода | ✅ Настроено |
| Health checks | ✅ Настроено |
| PostgreSQL + Redis | ✅ Настроено |
| Development overrides | ✅ compose.override.yml |

Готово к продуктивной разработке! 🎉
