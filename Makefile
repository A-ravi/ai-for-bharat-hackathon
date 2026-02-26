.PHONY: help build up down restart logs clean migrate test

help:
	@echo "Jal Sathi Development Commands"
	@echo "================================"
	@echo "make build     - Build all Docker containers"
	@echo "make up        - Start all services"
	@echo "make down      - Stop all services"
	@echo "make restart   - Restart all services"
	@echo "make logs      - View logs from all services"
	@echo "make clean     - Remove all containers and volumes"
	@echo "make migrate   - Run database migrations"
	@echo "make test      - Run all tests"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started. Frontend: http://localhost:3000, Backend: http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

migrate:
	docker-compose exec backend alembic upgrade head
	@echo "Database migrations applied"

test:
	docker-compose exec backend pytest
	docker-compose exec frontend npm test
