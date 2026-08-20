# Escenario 4 — Ejercicio: CI/CD FastAPI

![CI/CD](https://github.com/jhoncardona-dev/Mi-Proyecto/actions/workflows/ci-cd.yml/badge.svg)

Aplicación **FastAPI** con multi-stage Dockerfile, tests, Trivy, publicación a DockerHub y GHCR.

## Requisitos cumplidos

- App en Python (FastAPI) en lugar de Node.js
- Workflow: tests → build → scan Trivy → push
- Tags semánticos (`v1.0.0`, `v1.0`, `latest`)
- Publicación en DockerHub **y** GHCR
- `docker-compose.prod.yml` con la imagen publicada
- Multi-stage build
- Scan de vulnerabilidades con Trivy
- Badge de estado del workflow

## Secrets necesarios en GitHub

Settings → Secrets and variables → Actions:

- `DOCKERHUB_USERNAME` (opcional pero recomendado)
- `DOCKERHUB_TOKEN` (opcional pero recomendado)

Sin esos secrets el workflow **igual publica en GHCR** (`ghcr.io/<usuario>/app-cicd-fastapi`).
Con ellos también publica en DockerHub.

## Probar localmente

```bash
cd escenario-4-cicd/ejercicio
docker compose up --build -d
curl http://localhost:8000/
curl http://localhost:8000/health

# Tests
pip install -r src/requirements.txt
pytest tests/ -v
```

## Producción con imagen publicada

```bash
export DOCKERHUB_USERNAME=tu-usuario
export TAG=latest
docker compose -f docker-compose.prod.yml up -d
```

## Nota sobre el workflow

El archivo de este ejercicio está en `.github/workflows/ci-cd.yml` (estructura del taller).
En la raíz del repositorio también existe `.github/workflows/ci-cd.yml` para que GitHub Actions lo detecte.
