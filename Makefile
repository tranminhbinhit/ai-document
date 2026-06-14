.PHONY: help start stop restart build clean logs status test

help:
	@echo "Document RAG System - Available Commands:"
	@echo ""
	@echo "  make start       - Start all services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make build       - Build all Docker images"
	@echo "  make clean       - Stop and remove all containers and volumes"
	@echo "  make logs        - View logs from all services"
	@echo "  make status      - Check status of all services"
	@echo "  make test        - Test API endpoints"
	@echo ""

start:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Waiting for services to initialize..."
	@sleep 10
	@make status

stop:
	@echo "Stopping all services..."
	docker-compose down

restart:
	@echo "Restarting all services..."
	docker-compose restart

build:
	@echo "Building all Docker images..."
	docker-compose build

clean:
	@echo "Cleaning up all containers and volumes..."
	docker-compose down -v
	@echo "Cleanup complete!"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-indexer:
	docker-compose logs -f indexer

logs-frontend:
	docker-compose logs -f frontend

status:
	@echo "Service Status:"
	@docker-compose ps

test:
	@echo "Testing API endpoints..."
	@echo ""
	@echo "Categories endpoint:"
	@curl -s http://localhost:5000/api/categories | head -n 20
	@echo ""
	@echo ""
	@echo "Health check - Backend:"
	@curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:5000/api/categories
	@echo ""
	@echo "Health check - Frontend:"
	@curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:4200
	@echo ""
	@echo "Health check - Qdrant:"
	@curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:6333/collections

init-db:
	@echo "Initializing database manually..."
	@bash scripts/manual-init.sh

reset-db:
	@echo "Resetting database completely..."
	@powershell -ExecutionPolicy Bypass -File scripts/reset-db.ps1

dev-backend:
	@echo "Starting backend in development mode..."
	cd backend/DocumentRAG.API && dotnet run

dev-frontend:
	@echo "Starting frontend in development mode..."
	cd frontend && npm start

dev-indexer:
	@echo "Starting indexer in development mode..."
	cd indexer && python worker.py
