.PHONY: install lint format check

install:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run python ../agent-dev-harness/python-styleguide/docstring_length.py .
	uv run mypy .

run:
	docker compose up

build-db:
	docker compose build db

build-app:
	docker-compose build app

refresh-data:
	docker compose restart app

db-connect: 
	psql postgresql://postgres:postgres@0.0.0.0:5433/activities

