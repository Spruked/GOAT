# GOAT - Greatest Of All Time
# Courtroom-Grade AI Evidence Preparation System
# Docker Development Makefile

.PHONY: help build up down restart logs clean test prod-up prod-down backup restore

# Default target
help: ## Show this help message
	@echo "GOAT Docker Development Commands"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development commands
build: ## Build the development containers
	docker-compose build

up: ## Start the development environment
	docker-compose up -d

down: ## Stop the development environment
	docker-compose down

restart: ## Restart the development environment
	docker-compose restart

logs: ## Show logs from the development environment
	docker-compose logs -f

shell: ## Open a shell in the backend container
	docker-compose exec goat-backend bash

shell-db: ## Open a shell in the database container
	docker-compose exec goat-db psql -U goat -d goat

shell-redis: ## Open a shell in the Redis container
	docker-compose exec goat-redis redis-cli

# Testing commands
test: ## Run tests in the test environment
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit

test-build: ## Build the test containers
	docker-compose -f docker-compose.test.yml build

test-up: ## Start the test environment
	docker-compose -f docker-compose.test.yml up -d

test-down: ## Stop the test environment
	docker-compose -f docker-compose.test.yml down

# Production commands
prod-build: ## Build the production containers
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start the production environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop the production environment
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## Show logs from the production environment
	docker-compose -f docker-compose.prod.yml logs -f

prod-restart: ## Restart the production environment
	docker-compose -f docker-compose.prod.yml restart

# Database commands
db-backup: ## Backup the production database
	docker-compose -f docker-compose.prod.yml exec goat-db pg_dump -U goat -d goat > goat_backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore: ## Restore database from backup (usage: make db-restore FILE=backup.sql)
	docker-compose -f docker-compose.prod.yml exec -T goat-db psql -U goat -d goat < $(FILE)

db-migrate: ## Run database migrations
	docker-compose exec goat-backend python -m alembic upgrade head

# Cleanup commands
clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all
	docker-compose -f docker-compose.test.yml down -v --rmi all
	docker-compose -f docker-compose.prod.yml down -v --rmi all

clean-volumes: ## Remove all Docker volumes
	docker volume rm $$(docker volume ls -q | grep goat) 2>/dev/null || true

clean-images: ## Remove all GOAT-related Docker images
	docker images | grep goat | awk '{print $$3}' | xargs docker rmi 2>/dev/null || true

# Health check
health: ## Check the health of all services
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/health || echo "Backend not healthy"
	@echo "Checking database..."
	@docker-compose exec goat-db pg_isready -U goat -d goat || echo "Database not ready"
	@echo "Checking Redis..."
	@docker-compose exec goat-redis redis-cli ping || echo "Redis not responding"

# Development utilities
format: ## Format Python code
	docker-compose exec goat-backend black .
	docker-compose exec goat-backend isort .

lint: ## Lint Python code
	docker-compose exec goat-backend flake8 .
	docker-compose exec goat-backend mypy .

security: ## Run security checks
	docker-compose exec goat-backend bandit -r .

deps: ## Update Python dependencies
	docker-compose exec goat-backend pip-compile --upgrade
	docker-compose exec goat-backend pip-sync

# Monitoring
monitor: ## Show resource usage
	docker stats $$(docker-compose ps -q)

top: ## Show running processes
	docker-compose top

# Environment setup
setup: ## Initial setup for development
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
	@echo "Then run: make build && make up"

# Quick start
quickstart: setup build up ## Quick start development environment
	@echo "GOAT development environment is starting..."
	@echo "Backend will be available at: http://localhost:8000"
	@echo "API documentation at: http://localhost:8000/docs"
	@echo "Health check at: http://localhost:8000/health"