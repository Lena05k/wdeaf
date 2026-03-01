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

log "Running backend migrations..."
docker compose exec -T backend python manage.py migrate

log "Running backend tests..."
docker compose exec -T backend python manage.py test api.tests --verbosity=2

log "Running frontend build..."
docker compose exec -T frontend npm run build

log "All local checks passed."
