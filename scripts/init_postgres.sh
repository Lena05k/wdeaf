#!/bin/bash
# Автоматическая проверка и исправление проблем с PostgreSQL при запуске

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}$1${NC}"
}

log_success() {
    echo -e "${GREEN}$1${NC}"
}

log_warning() {
    echo -e "${YELLOW}$1${NC}"
}

log_error() {
    echo -e "${RED}$1${NC}"
}

# Загружаем .env если существует
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Переменные для подключения к PostgreSQL
PG_SUPER_USER=${POSTGRES_USER:-postgres}
PG_SUPER_PASSWORD=${POSTGRES_PASSWORD:-secure_db_password_change_this}
DB_USER=${DB_USER:-wdeaf_user}
DB_NAME=${DB_NAME:-wdeaf_db}
DB_PASSWORD=${DB_PASSWORD:-secure_db_password_change_this}

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}WDEAF - Проверка PostgreSQL${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Проверяем, запущен ли PostgreSQL
if ! docker compose ps | grep -q "wdeaf-postgres.*Up"; then
    log_info "PostgreSQL не запущен. Запуск..."
    docker compose up -d postgres
    sleep 5
fi

# Ждем пока PostgreSQL будет готов (до 60 секунд)
log_info "Ожидание готовности PostgreSQL..."
for i in {1..60}; do
    if docker compose exec -T postgres pg_isready -q 2>/dev/null; then
        log_success "PostgreSQL готов"
        break
    fi
    if [ $i -eq 60 ]; then
        log_error "PostgreSQL не отвечает после 60 секунд"
        exit 1
    fi
    sleep 1
done

# Функция для выполнения команд psql от имени суперпользователя
psql_super() {
    docker compose exec -T postgres psql -U "$PG_SUPER_USER" -d postgres -c "$1" 2>/dev/null
}

# Проверяем существование пользователя БД
log_info "Проверка пользователя ${DB_USER}..."
if ! psql_super "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}';" | grep -q "1"; then
    log_warning "Пользователь ${DB_USER} не существует. Создание..."
    psql_super "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" || true
fi

# Проверяем существование базы данных
log_info "Проверка базы данных ${DB_NAME}..."
if ! psql_super "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}';" | grep -q "1"; then
    log_warning "База данных ${DB_NAME} не существует. Создание..."
    psql_super "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};" || true
fi

# Проверяем права доступа
log_info "Проверка прав доступа..."
psql_super "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};" 2>/dev/null || true

# Предоставляем права на схему public (необходимо для PostgreSQL 15+)
log_info "Предоставление прав на схему public..."
psql_super "GRANT ALL ON SCHEMA public TO ${DB_USER};" 2>/dev/null || true
psql_super "GRANT ALL ON ALL TABLES IN SCHEMA public TO ${DB_USER};" 2>/dev/null || true
psql_super "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ${DB_USER};" 2>/dev/null || true

# Проверяем аутентификацию пользователя
log_info "Проверка аутентификации..."
if ! docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    log_error "Ошибка аутентификации пользователя ${DB_USER}"
    echo ""
    log_warning "Возможная причина: старый том Docker с другим паролем"
    log_info "Сброс volumes и пересоздание БД..."
    echo ""
    
    docker compose down -v
    
    log_info "Пересоздание контейнеров..."
    docker compose up -d
    
    # Ждем пока PostgreSQL будет готов
    for i in {1..60}; do
        if docker compose exec -T postgres pg_isready -q 2>/dev/null; then
            break
        fi
        if [ $i -eq 60 ]; then
            log_error "PostgreSQL не запустился"
            exit 1
        fi
        sleep 1
    done
    
    log_success "БД пересоздана!"
else
    log_success "Аутентификация успешна"
fi

echo ""
log_success "PostgreSQL полностью готов к работе!"
echo ""
