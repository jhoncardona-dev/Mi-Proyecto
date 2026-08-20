.PHONY: up down build logs restart test-api

up:
	docker compose up -d

build:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart

test-api:
	curl -s http://localhost:3000/health
	@echo ""
	curl -s -X POST http://localhost:3000/usuarios -H "Content-Type: application/json" -d "{\"nombre\":\"Juan\",\"email\":\"juan@test.com\"}"
	@echo ""
	curl -s http://localhost:3000/usuarios
	@echo ""
