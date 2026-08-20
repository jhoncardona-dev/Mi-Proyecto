# Escenario 3 — Ejercicio: FastAPI + Redis + PostgreSQL

Aplicación con caché Redis, rate limiting, contador de visitas y PostgreSQL como fuente de verdad.

## Requisitos cumplidos

- FastAPI en lugar de Flask
- Endpoint `/contador` con `INCR`
- Rate limiting: máx. 10 requests/minuto por IP
- PostgreSQL como fuente de verdad; Redis como caché
- `/usuarios` busca primero en Redis, luego en PostgreSQL
- `docker-compose.override.yml` para desarrollo
- Healthchecks en todos los servicios

## Levantar (desarrollo)

```bash
cd escenario-3-redis-cache/ejercicio
docker compose up --build -d
# Docker Compose aplica automáticamente docker-compose.override.yml
```

- API: http://localhost:5000
- Docs: http://localhost:5000/docs
- Redis Commander (dev): http://localhost:8082

## Producción (sin override)

```bash
docker compose -f docker-compose.yml up --build -d
```

## Probar

```bash
curl http://localhost:5000/
curl http://localhost:5000/contador
curl http://localhost:5000/datos
curl http://localhost:5000/usuarios
curl http://localhost:5000/health
```
