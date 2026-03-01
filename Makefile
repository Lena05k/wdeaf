.PHONY: help up up-safe init-db down rebuild rebuild-no-cache logs shell test migrate reset-db clean reset-volumes check-db

# Справка по командам
help:
	@echo "WDEAF Project Commands"
	@echo ""
	@echo "  make up          - Запуск всех сервисов (frontend + backend + db + redis)"
	@echo "  make up-safe     - Запуск с авто-исправлением проблем БД"
	@echo "  make init-db     - Инициализация/сброс PostgreSQL (проверка пароля, пользователя, БД)"
	@echo "  make down        - Остановка всех сервисов"
	@echo "  make rebuild     - Пересборка и запуск всех сервисов"
	@echo "  make rebuild-no-cache - Пересборка без кэша и запуск всех сервисов"
	@echo "  make check-db    - Проверка подключения к PostgreSQL"
	@echo "  make reset-volumes - Остановка и удаление всех volumes (БД, Redis)"
	@echo "  make logs        - Просмотр логов всех сервисов"
	@echo "  make logs-backend- Логи backend"
	@echo "  make logs-frontend - Логи frontend"
	@echo "  make shell-backend - Shell в backend контейнере"
	@echo "  make shell-frontend - Shell в frontend контейнере"
	@echo "  make test        - Запуск тестов backend"
	@echo "  make migrate     - Применение миграций backend"
	@echo "  make reset-db    - Полная очистка БД и миграции"
	@echo "  make clean       - Остановка и очистка volumes"

# Запуск всех сервисов
up:
	docker compose up -d postgres redis
	@echo "Ожидание готовности PostgreSQL..."
	@sleep 15
	@echo "Инициализация PostgreSQL..."
	@./scripts/init_postgres.sh
	@echo "Ожидание применения прав..."
	@sleep 5
	@echo "Запуск backend и frontend..."
	docker compose up -d backend frontend
	@sleep 5
	@echo "Готово!"
	@docker compose ps

# Запуск с автоматической проверкой и исправлением проблем БД
up-safe:
	docker compose down -v
	docker compose up -d postgres redis
	@echo "Ожидание готовности PostgreSQL..."
	@sleep 15
	@echo "Инициализация PostgreSQL..."
	@./scripts/init_postgres.sh
	@echo "Ожидание применения прав..."
	@sleep 5
	@echo "Запуск backend и frontend..."
	docker compose up -d backend frontend
	@sleep 5
	@echo "Готово!"
	@docker compose ps

# Инициализация PostgreSQL (проверка и создание пользователя/БД)
init-db:
	@./scripts/init_postgres.sh

# Остановка сервисов
down:
	docker compose down

# Пересборка и запуск
rebuild:
	docker compose down
	docker compose up -d postgres redis
	@echo "Ожидание готовности PostgreSQL..."
	@sleep 15
	@echo "Инициализация PostgreSQL..."
	@./scripts/init_postgres.sh
	@echo "Ожидание применения прав..."
	@sleep 5
	@echo "Запуск backend и frontend..."
	docker compose up -d --build backend frontend
	@sleep 5
	@echo "Готово!"
	@docker compose ps

# Пересборка без кэша и запуск
rebuild-no-cache:
	docker compose down
	docker compose build --no-cache
	docker compose up -d postgres redis
	@echo "Ожидание готовности PostgreSQL..."
	@sleep 15
	@echo "Инициализация PostgreSQL..."
	@./scripts/init_postgres.sh
	@echo "Ожидание применения прав..."
	@sleep 5
	@echo "Запуск backend и frontend..."
	docker compose up -d backend frontend
	@sleep 5
	@echo "Готово!"
	@docker compose ps

# Проверка подключения к PostgreSQL
check-db:
	@./scripts/check_db.sh

# Логи всех сервисов
logs:
	docker compose logs -f

# Логи backend
logs-backend:
	docker compose logs -f backend

# Логи frontend
logs-frontend:
	docker compose logs -f frontend

# Shell в backend
shell-backend:
	docker compose exec backend bash

# Shell в frontend
shell-frontend:
	docker compose exec frontend sh

# Тесты backend
test:
	docker compose exec backend python manage.py test api.tests

# Миграции backend
migrate:
	docker compose exec backend python manage.py migrate

# Полная очистка БД и миграции
reset-db:
	docker compose exec backend python manage.py flush --no-input
	docker compose exec backend python manage.py migrate
	docker compose exec backend python manage.py shell -c "from api.models import User; User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='adminadmin', first_name='Admin')"
	@echo ""
	@echo "✅ Database reset complete!"
	@echo "📝 Superuser created: admin@example.com / adminadmin"

# Остановка и очистка volumes
clean:
	docker compose down -v

# Сброс volumes (БД и Redis) - полезно при проблемах с паролем/версией PostgreSQL
reset-volumes:
	docker compose down -v
	docker compose up -d
	@echo ""
	@echo "✅ Volumes сброшены. БД пересоздана с новыми учетными данными."
