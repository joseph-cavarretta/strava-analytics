FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=activities

COPY ./sql/create_database.sql /docker-entrypoint-initdb.d/create_database.sql