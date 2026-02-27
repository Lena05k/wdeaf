.PHONY: help up up-dev up-build down rebuild rebuild-cache migrate shell test logs logs-backend logs-db superuser start clean

# Справка по доступным командам (вызывается по умолчанию)
help:
	@echo "Docker Compose команды для проекта:"
	@echo ""
	@echo "  make up           - Запуск контейнеров с логами (foreground)"
	@echo "  make up-dev       - Запуск с пересборкой и логами (foreground)"
	@echo "  make up-build     - Запуск с пересборкой образов и логами"
	@echo "  make down         - Остановка контейнеров"
	@echo "  make rebuild      - Пересборка с очисткой кэша и запуск с логами"
	@echo "  make rebuild-cache- Запуск с пересборкой с сохранением кэша (быстро)"
	@echo "  make start        - Быстрый старт: сборка + миграции + суперпользователь (admin/admin)"
	@echo "  make migrate      - Применение миграций"
	@echo "  make shell        - Открыть shell в контейнере backend"
	@echo "  make test         - Запуск тестов Django"
	@echo "  make logs         - Просмотр логов всех сервисов"
	@echo "  make logs-backend - Просмотр логов backend"
	@echo "  make logs-db      - Просмотр логов базы данных"
	@echo "  make superuser    - Создание суперпользователя admin/admin"
	@echo "  make clean        - Остановка и очистка volumes"
	@echo ""

# Запуск по умолчанию
.DEFAULT_GOAL := help

# Запуск контейнеров с логами (foreground)
up:
	docker compose up

# Запуск контейнеров в foreground с логами и пересборкой (для разработки)
up-dev:
	docker compose up --build

# Запуск контейнеров с пересборкой и логами
up-build:
	docker compose up --build

# Остановка контейнеров
down:
	docker compose down

# Пересборка и запуск контейнеров (полная, без кэша) с логами
rebuild:
	docker compose down
	docker compose build --no-cache
	docker compose up

# Пересборка с сохранением кэша (быстрый запуск) с логами
rebuild-cache:
	docker compose up --build

# Применение миграций
migrate:
	docker compose exec backend python manage.py migrate

# Открыть shell в контейнере
shell:
	docker compose exec backend sh

# Запуск тестов
test:
	docker compose exec backend python manage.py test

# Просмотр логов
logs:
	docker compose logs -f

# Логи конкретного сервиса
logs-backend:
	docker compose logs -f backend

logs-db:
	docker compose logs -f db

# Создание суперпользователя admin/admin
superuser:
	docker compose exec backend python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Быстрый старт: сборка, миграции, суперпользователь (с логами)
start:
	docker compose up --build &
	sleep 5
	docker compose exec backend python manage.py migrate
	docker compose exec backend python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Остановка и очистка volumes
clean:
	docker compose down -v
