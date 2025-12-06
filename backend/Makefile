.PHONY: help install dev test test-verbose clean seed lint format

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies using uv"
	@echo "  make dev          - Run development server with auto-reload"
	@echo "  make test         - Run all tests"
	@echo "  make test-verbose - Run tests with verbose output"
	@echo "  make seed         - Seed database with sample data"
	@echo "  make clean        - Remove cache and temporary files"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code"

install:
	uv sync

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest tests/

test-verbose:
	uv run pytest tests/ -v

test-coverage:
	uv run pytest tests/ --cov=app --cov-report=term-missing

seed:
	uv run python seed_data.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	uv run ruff check app/ tests/

format:
	uv run ruff format app/ tests/
