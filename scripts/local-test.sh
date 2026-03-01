#!/bin/bash
#
# Local CI script for the root project.
# Runs backend migrations/tests and frontend build via docker compose.
#

set -euo pipefail

QUIET=false
if [[ "${1:-}" == "--quiet" ]]; then
  QUIET=true
fi

log() {
  if [[ "$QUIET" == "false" ]]; then
    echo "$1"
  fi
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f ".env" ]]; then
  log "Creating .env from .env.example..."
  cp .env.example .env
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not running."
  exit 1
fi

log "Starting containers..."
docker compose up -d

log "Waiting for PostgreSQL to initialize..."
# Load .env variables into the shell environment for the next commands
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi
# Wait until postgres is ready
until docker compose exec postgres pg_isready -U "$POSTGRES_USER" -d "$DB_NAME" -q; do
  log "PostgreSQL is unavailable - sleeping"
  sleep 1
done
log "PostgreSQL is up - creating user and granting permissions"

docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$DB_NAME" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD' CREATEDB;" || true
docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$DB_NAME" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;"
docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$DB_NAME" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;"

log "Running backend migrations..."
docker compose exec -T backend python manage.py migrate

log "Running backend tests..."
docker compose exec -T backend python manage.py test api.tests --verbosity=2

log "Running frontend build..."
docker compose exec -T frontend npm run build

log "All local checks passed."
