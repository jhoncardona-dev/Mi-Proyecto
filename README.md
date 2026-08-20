# Taller Práctico: Docker + Git

Repositorio del taller **Docker + Git** (4 escenarios progresivos).

## Estructura

```
Mi-Proyecto/
├── README.md
├── .gitignore
├── docs/
│   ├── git-workflow.md
│   └── docker-commands.md
├── escenario-1-wordpress/   # WordPress + MariaDB + phpMyAdmin
├── escenario-2-api-node/    # API REST Node.js + PostgreSQL
├── escenario-3-redis-cache/ # FastAPI + Redis + PostgreSQL
└── escenario-4-cicd/        # CI/CD GitHub Actions → DockerHub/GHCR
```

Cada escenario incluye:

- `ejemplo/` — solución guiada de la guía
- `ejercicio/` — solución del estudiante con los requisitos solicitados

## Ramas

| Rama | Contenido |
|------|-----------|
| `master` | Documentación y merge final |
| `escenario-1-wordpress` | Escenario 1 |
| `escenario-2-api-node` | Escenario 2 |
| `escenario-3-redis` | Escenario 3 |
| `escenario-4-cicd` | Escenario 4 |

## Cómo empezar

```bash
git clone https://github.com/jhoncardona-dev/Mi-Proyecto.git
cd Mi-Proyecto
```

Entra a cada carpeta `ejercicio/` y sigue el `README.md` local.

## Documentación adicional

- [Flujo Git](docs/git-workflow.md)
- [Comandos Docker](docs/docker-commands.md)
