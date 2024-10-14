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

