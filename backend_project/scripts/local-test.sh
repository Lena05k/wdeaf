#!/bin/bash
#
# Local test script for pre-commit testing
# Usage: ./scripts/local-test.sh
#
# This script runs the same tests as GitHub Actions
# Run this before committing to catch issues early
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Local Test Suite (Pre-commit)${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if .env exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
fi

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Step 1: Starting Docker containers...${NC}"
cd "$PROJECT_DIR"
docker compose up -d db redis
echo "Waiting for databases to be ready (10 seconds)..."
sleep 10

echo ""
echo -e "${YELLOW}🔧 Step 2: Running migrations...${NC}"
docker compose exec -T backend python manage.py migrate

echo ""
echo -e "${YELLOW}🧪 Step 3: Running tests...${NC}"
docker compose exec -T backend python manage.py test api.tests --verbosity=2

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✅ All tests passed!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "You can now safely commit and push your changes."
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  ❌ Some tests failed!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Please fix the failing tests before committing."
fi

echo ""
echo -e "${YELLOW}💡 Tip: You can also run individual tests:${NC}"
echo "   docker compose exec backend python manage.py test api.tests.AuthTestCase.test_01_signup"
echo ""

# Cleanup (optional - comment out to keep containers running)
# echo -e "${YELLOW}🧹 Cleaning up...${NC}"
# docker compose down

exit $TEST_RESULT
