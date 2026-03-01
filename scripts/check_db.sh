#!/bin/bash
# Проверка подключения к PostgreSQL и автоматический сброс при ошибке аутентификации

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Проверка подключения к PostgreSQL...${NC}"
echo ""

# Ждем пока PostgreSQL будет готов (до 30 секунд)
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -q 2>/dev/null; then
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Ошибка: PostgreSQL не отвечает после 30 секунд${NC}"
        exit 1
    fi
    sleep 1
done

# Получаем переменные окружения из .env или используем значения по умолчанию
source_if_exists() {
    if [ -f "$1" ]; then
        export $(grep -v '^#' "$1" | xargs)
    fi
}

# Загружаем .env если существует
source_if_exists ".env"

DB_USER=${DB_USER:-wdeaf_user}
DB_NAME=${DB_NAME:-wdeaf_db}

# Проверяем аутентификацию пользователя
if ! docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${RED}Ошибка аутентификации пользователя ${DB_USER}${NC}"
    echo ""
    echo "Возможные причины:"
    echo "  1. Старый том Docker с другим паролем"
    echo "  2. Изменен пароль в .env после первого запуска"
    echo "  3. Конфликт версий PostgreSQL (данные от другой версии)"
    echo ""
    echo -e "${YELLOW}Автоматический сброс volumes через 2 секунды...${NC}"
    sleep 2
    
    echo "Удаление volumes..."
    docker compose down -v
    
    echo "Пересоздание контейнеров..."
    docker compose up -d
    
    # Ждем пока PostgreSQL будет готов
    for i in {1..30}; do
        if docker compose exec -T postgres pg_isready -q 2>/dev/null; then
            break
        fi
        if [ $i -eq 30 ]; then
            echo -e "${RED}Ошибка: PostgreSQL не запустился${NC}"
            exit 1
        fi
        sleep 1
    done
    
    echo -e "${GREEN}БД пересоздана!${NC}"
else
    echo -e "${GREEN}PostgreSQL доступен и аутентификация успешна${NC}"
fi

echo ""
