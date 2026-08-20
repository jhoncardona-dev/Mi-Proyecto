# Flujo de trabajo Git

## Ramas del taller

| Rama | Propósito |
|------|-----------|
| `master` / `main` | Documentación general, README, guías |
| `escenario-1-wordpress` | Desarrollo del Escenario 1 |
| `escenario-2-api-node` | Desarrollo del Escenario 2 |
| `escenario-3-redis` | Desarrollo del Escenario 3 |
| `escenario-4-cicd` | Desarrollo del Escenario 4 |

## Flujo por escenario

```bash
git checkout -b escenario-1-wordpress
# ... trabajar en escenario-1-wordpress/ejercicio/
git add .
git commit -m "feat: agrega docker-compose para WordPress + MariaDB"
git push origin escenario-1-wordpress
git checkout master
git merge escenario-1-wordpress
```

## Convención de commits

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` documentación
- `refactor:` refactorización
- `test:` pruebas
- `chore:` mantenimiento
