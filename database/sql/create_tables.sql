-- sudo su - postgres
-- psql -U postgres -v ON_ERROR_STOP=1 -h 127.0.0.1 -f create_tables.sql
\c activities;

DROP TABLE IF EXISTS activities_raw;
DROP TABLE IF EXISTS activities_processed;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS dates;

DO $$ BEGIN
    CREATE TYPE type_label AS ENUM ('aerobic', 'non-aerobic', 'omit');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE activities_raw (
    id                    BIGINT PRIMARY KEY, 
    name                  TEXT,
    start_date            VARCHAR(30),
    start_date_local      VARCHAR(30), 
    type                  VARCHAR(30), 
    distance              NUMERIC(14,1),
    distance_units        VARCHAR(10),
    moving_time           INTEGER,
    elapsed_time          INTEGER,
    time_units            VARCHAR(10), 
    total_elevation_gain  NUMERIC(14,1),
    elevation_units       VARCHAR(10)
);


CREATE TABLE activities_processed (
    id                    BIGINT PRIMARY KEY, 
    name                  TEXT,
    type                  VARCHAR(30),
    miles                 NUMERIC(6,2),
    moving_time_sec       INTEGER,
    elapsed_time_sec      INTEGER,
    hours                 NUMERIC(10,2),
    elevation_gain_ft     NUMERIC(10,2),
    start_date            VARCHAR(30), 
    start_date_local      VARCHAR(30), 
    date                  DATE,
    year                  SMALLINT,
    month                 SMALLINT,
    day_of_month          SMALLINT,
    week_of_year          SMALLINT,
    day_of_year           SMALLINT,
    year_week             VARCHAR(10),
    route1_name           VARCHAR(20),
    route1_count          SMALLINT,
    route2_name           VARCHAR(20),
    route2_count          SMALLINT,
    route3_name           VARCHAR(20),
    route3_count          SMALLINT
);

CREATE TABLE activities (
    id                    BIGINT PRIMARY KEY, 
    date_id               DATE,
    type_id               SMALLINT,
    name                  TEXT,
    miles                 NUMERIC(6,2),
    hours                 NUMERIC(10,2),
    moving_time_sec       INTEGER,
    elapsed_time_sec      INTEGER,
    elevation_gain_ft     NUMERIC(10,2),
    start_date_local      VARCHAR(30)
);


CREATE TABLE types (
    id                    SERIAL PRIMARY KEY,
    type_id               INTEGER NOT NULL,
    type_name                  TEXT,
    label                 TYPE_LABEL
);


CREATE TABLE dates (
    id                    SERIAL PRIMARY KEY,
    date_id               DATE NOT NULL,
    year                  SMALLINT,
    month                 SMALLINT,
    day_of_month          SMALLINT,
    week_of_year          SMALLINT,
    day_of_year           SMALLINT,
    year_week             VARCHAR(10)
);


CREATE TABLE counts (
    id                    SERIAL PRIMARY KEY,
    activity_id           BIGINT NOT NULL,
    route1_name           VARCHAR(20),
    route1_count          SMALLINT,
    route2_name           VARCHAR(20),
    route2_count          SMALLINT,
    route3_name           VARCHAR(20),
    route3_count          SMALLINT
);