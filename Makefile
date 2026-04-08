.PHONY: help install install-dev lint format test run db-init db-migrate db-upgrade seed clean pre-commit-init

help:
	@echo "StockFlow Development Commands"
	@echo "=============================="
	@echo "make install          Install production dependencies"
	@echo "make install-dev      Install development dependencies"
	@echo "make lint             Run code quality checks (ruff, mypy)"
	@echo "make format           Auto-format code (black, isort)"
	@echo "make test             Run test suite with coverage"
	@echo "make run              Start development server"
	@echo "make db-init          Initialize database migrations"
	@echo "make db-migrate       Create database migration"
	@echo "make db-upgrade       Apply database migrations"
	@echo "make seed             Load sample data"
	@echo "make clean            Remove build artifacts and cache"
	@echo "make pre-commit-init  Install pre-commit hooks"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check app tests
	black --check app tests
	@echo "Linting passed!"

format:
	isort app tests
	black app tests
	ruff check --fix app tests
	@echo "Code formatted!"

test:
	pytest --cov=app --cov-report=html --cov-report=term-missing tests/

run:
	python run.py

db-init:
	flask db init

db-migrate:
	@read -p "Enter migration message: " msg; \
	flask db migrate -m "$$msg"

db-upgrade:
	flask db upgrade

seed:
	flask seed-data

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .coverage -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -type d -name *.egg-info -exec rm -rf {} +

pre-commit-init:
	pre-commit install
	pre-commit run --all-files

.DEFAULT_GOAL := help
