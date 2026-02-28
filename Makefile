.PHONY: help up down rebuild logs shell test migrate reset-db clean

# Справка по командам
help:
	@echo "WDEAF Project Commands"
	@echo ""
	@echo "  make up          - Запуск всех сервисов (frontend + backend + db + redis)"
	@echo "  make down        - Остановка всех сервисов"
	@echo "  make rebuild     - Пересборка и запуск всех сервисов"
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
	docker compose up -d

# Остановка сервисов
down:
	docker compose down

# Пересборка и запуск
rebuild:
	docker compose down
	docker compose up -d --build

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
