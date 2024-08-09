DROP DATABASE IF EXISTS activities;

CREATE DATABASE activities;
\c activities;

CREATE TABLE activities_raw (
    `id`                    BIGINT PRIMARY KEY, 
    `name`                  VARCHAR(99),
    `start_date`            VARCHAR(30),
    `start_date_local`      VARCHAR(30), 
    `type`                  VARCHAR(30), 
    `distance`              NUMERIC(14,1),
    `distance_units`        VARCHAR(10),
    `moving_time`           INTEGER, 
    `elapsed_time`          INTEGER,
    `time_units`            VARCHAR(10), 
    `total_elevation_gain`  NUMERIC(14,1),
    `elevation_units`       VARCHAR(10)
);


CREATE TABLE activies_processed (
    `id`                    BIGINT PRIMARY KEY, 
    `name`                  VARCHAR(99),
    `type`                  VARCHAR(30),
    `miles`                 NUMERIC(6,2),
    `moving_time_sec`       INTEGER,
    `elapsed_time_sec`      INTEGER,
    `hours`                 NUMERIC(10,2),
    `elevation_gain_ft`     NUMERIC(10,2),
    `start_date`            VARCHAR(30), 
    `start_date_local`      VARCHAR(30), 
    `date`                  DATE,
    `year`                  SMALLINT,
    `month`                 SMALLINT,
    `day_of_month`          SMALLINT,
    `week_of_year`          SMALLINT,
    `day_of_year`           SMALLINT,
    `year_week`             VARCHAR(10),
    `bear_peak_count`       SMALLINT,
    `sanitas_count`         SMALLINT,
    `second_flatiron_count` SMALLINT
);

CREATE TABLE activity (
    `id`                    BIGINT PRIMARY KEY, 
    `date_id`               DATE,
    `type_id`               SMALLINT,
    `name`                  VARCHAR(99),
    `miles`                 NUMERIC(6,2),
    `hours`                 NUMERIC(10,2),
    `moving_time_sec`       INTEGER,
    `elapsed_time_sec`      INTEGER,
    `elevation_gain_ft`     NUMERIC(10,2),
    `start_date_local`      VARCHAR(30)
);


CREATE TABLE type (
    `id`                    SERIAL PRIMARY KEY,
    `type_id`               INTEGER NOT NULL,
    `name`                  VARCHAR(99)
);


CREATE TABLE date (
    `id`                    SERIAL PRIMARY KEY,
    `date_id`               DATE NOT NULL,
    `year`                  SMALLINT,
    `month`                 SMALLINT,
    `day_of_month`          SMALLINT,
    `week_of_year`          SMALLINT,
    `day_of_year`           SMALLINT,
    `year_week`             VARCHAR(10)
);


CREATE TABLE counts (
    `id`                    SERIAL PRIMARY KEY,
    `activity_id`           BIGINT NOT NULL,
    `route1_name`           VARCHAR(20),
    `route1_count`          SMALLINT,
    `route2_name`           VARCHAR(20),
    `route2_count`          SMALLINT,
    `route3_name`           VARCHAR(20),
    `route3_count`          SMALLINT
);