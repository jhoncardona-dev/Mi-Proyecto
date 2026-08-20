# Escenario 1 — Ejercicio: WordPress + MariaDB + phpMyAdmin

Stack con **MariaDB**, **WordPress** y **phpMyAdmin**, variables en `.env`, volumen `mi_wordpress_data` y red `mi_red_wordpress`.

## Requisitos cumplidos

- MariaDB (`mariadb:10.11`) en lugar de MySQL
- phpMyAdmin en puerto **8081**
- Variables de entorno desde `.env`
- Volumen nombrado `mi_wordpress_data`
- Red `mi_red_wordpress`

## Cómo levantar

```bash
cd escenario-1-wordpress/ejercicio
docker compose up -d
```

- WordPress: http://localhost:8080
- phpMyAdmin: http://localhost:8081

## Logs y detener

```bash
docker compose logs -f
docker compose down        # detener
docker compose down -v     # detener y borrar volúmenes
```

## Credenciales (archivo `.env`)

| Variable | Valor demo |
|----------|------------|
| MYSQL_USER | wpuser |
| MYSQL_PASSWORD | wppassword |
| MYSQL_DATABASE | wordpress |
