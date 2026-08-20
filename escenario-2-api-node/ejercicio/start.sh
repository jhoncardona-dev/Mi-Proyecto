#!/usr/bin/env bash
set -euo pipefail

case "${1:-up}" in
  up)
    docker compose up -d
    ;;
  build)
    docker compose up --build -d
    ;;
  down)
    docker compose down
    ;;
  logs)
    docker compose logs -f
    ;;
  test)
    curl -s http://localhost:3000/health
    echo
    curl -s -X POST http://localhost:3000/usuarios \
      -H "Content-Type: application/json" \
      -d '{"nombre":"Juan","email":"juan@test.com"}'
    echo
    curl -s http://localhost:3000/usuarios
    echo
    ;;
  *)
    echo "Uso: ./start.sh [up|build|down|logs|test]"
    exit 1
    ;;
esac
