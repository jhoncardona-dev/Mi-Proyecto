# Cheatsheet Docker Compose

```bash
# Levantar servicios
docker compose up -d
docker compose up --build -d
docker compose up -d --scale api=3

# Estado y logs
docker compose ps
docker compose logs -f [servicio]
docker compose top

# Gestión
docker compose stop
docker compose start
docker compose restart [servicio]
docker compose down
docker compose down -v

# Inspección
docker compose exec [servicio] sh
docker compose exec db psql -U postgres
docker compose exec redis redis-cli

# Limpieza
docker system prune -f
docker volume prune -f
docker compose down --rmi all -v
```
