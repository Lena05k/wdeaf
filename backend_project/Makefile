.PHONY: help up up-dev up-build down rebuild rebuild-cache migrate migrate-reset shell test test-verbose logs logs-backend logs-db superuser reset-db start clean

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
	@echo "  make migrate-reset- Полная очистка БД + миграции + суперпользователь"
	@echo "  make shell        - Открыть shell в контейнере backend"
	@echo "  make test         - Запуск тестов Django"
	@echo "  make test-verbose - Запуск тестов с подробным выводом"
	@echo "  make logs         - Просмотр логов всех сервисов"
	@echo "  make logs-backend - Просмотр логов backend"
	@echo "  make logs-db      - Просмотр логов базы данных"
	@echo "  make superuser    - Создание суперпользователя admin/admin"
	@echo "  make reset-db     - Полная очистка БД, миграции, суперпользователь"
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
	docker compose exec backend python manage.py test api.tests

# Запуск тестов с подробным выводом
test-verbose:
	docker compose exec backend python manage.py test api.tests --verbosity=2

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
	docker compose exec backend python manage.py shell -c "from api.models import User; User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='adminadmin', first_name='Admin')"

# Полная очистка БД, миграции, суперпользователь
reset-db:
	@echo "=== Полная очистка базы данных ==="
	docker compose exec backend python manage.py flush --no-input
	@echo "=== Применение миграций ==="
	docker compose exec backend python manage.py migrate
	@echo "=== Создание суперпользователя (admin@example.com / adminadmin) ==="
	docker compose exec backend python manage.py shell -c "from api.models import User; User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='adminadmin', first_name='Admin')"
	@echo "=== Готово! ==="

# Быстрый старт: сборка, миграции, суперпользователь (с логами)
start:
	docker compose up --build &
	sleep 5
	docker compose exec backend python manage.py migrate
	docker compose exec backend python manage.py shell -c "from api.models import User; User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='adminadmin', first_name='Admin')"

# Остановка и очистка volumes
clean:
	docker compose down -v
