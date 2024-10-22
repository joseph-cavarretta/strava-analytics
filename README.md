## Overview
This projects extracts,transforms, and models activity data from the Strava API into an interactive web dashboard. User activities are stored in a Postgres data warehouse hosted locally in Docker.

Apache Superset is hosted locally in Docker for dashboards and visualizations.

<p align="left">
<img width='1200' alt='Dashboard' src='https://github.com/joseph-cavarretta/photos/blob/dda92cc6fbd0562fbd982dc71561632a98f855f6/dashboard.png?raw=true'>
</p>


## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)


## Run App
Run `docker compose up` from the root of the project

## Dashboard
Apache Superset is cloned and run locally with Docker: [Apache Superset](https://superset.apache.org/)

## Direct Connect to Postgres Data Warehouse
```
psql postgres://postgres:postgres@0.0.0.0:5433/activities
```

## Developed by:
Joseph Cavarretta |
joseph.m.cavarretta@gmail.com |
[Github](https://github.com/joseph-cavarretta) |
[LinkedIn](https://www.linkedin.com/in/joseph-cavarretta-87242871/)
