# Escenario 2 — Ejercicio: API Node.js + PostgreSQL + pgAdmin

API REST con CRUD completo, migraciones SQL, validación de datos y pgAdmin.

## Requisitos cumplidos

- Endpoints `PUT /usuarios/:id` y `DELETE /usuarios/:id`
- Migración en `init-scripts/01-init.sql`
- Variables desde `.env`
- pgAdmin en puerto **5050**
- Validación básica de `nombre` y `email`
- `Makefile` y `start.sh` para comandos

## Levantar

```bash
cd escenario-2-api-node/ejercicio
make build
# o: docker compose up --build -d
# o: bash start.sh build
```

- API: http://localhost:3000
- pgAdmin: http://localhost:5050 (admin@example.com / admin123)

## Probar

```bash
curl http://localhost:3000/health
curl -X POST http://localhost:3000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana","email":"ana@test.com"}'
curl http://localhost:3000/usuarios
curl -X PUT http://localhost:3000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana Actualizada"}'
curl -X DELETE http://localhost:3000/usuarios/1
```
