-- to run: mysql -u root -p -e "source create_database.sql"

DROP DATABASE IF EXISTS `activities`;

CREATE DATABASE `activities`;
USE `activities`;

CREATE TABLE `activities`.`raw` (
    `id` INT NOT NULL PRIMARY KEY, 
    `name` VARCHAR(99),
    `start_date` VARCHAR(30),
    `start_date_local` VARCHAR(30), 
    `type` VARCHAR(30), 
    `distance` FLOAT(14,2),
    `distance_units` VARCHAR(10),
    `moving_time` INT, 
    `elapsed_time` INT,
    `time_units` VARCHAR(10), 
    `total_elevation_gain` FLOAT(14,2),
    `elevation_units` VARCHAR(10)
) engine=InnoDB;


CREATE TABLE `activities`.`processed` (
    `id` INT NOT NULL, 
    `name` VARCHAR(99),
    `type` VARCHAR(30),
    `miles` FLOAT(6,2),
    `moving_time_sec` INT,
    `elapsed_time_sec` INT,
    `hours` FLOAT(10,2),
    `elevation_gain_ft` FLOAT(10,2),
    `start_date` VARCHAR(30), 
    `start_date_local` VARCHAR(30), 
    `date` DATE,
    `year` INT,
    `month` INT,
    `day_of_month` INT,
    `week_of_year` INT,
    `day_of_year` INT,
    `year_week` VARCHAR(10),
    `bear_peak_count` INT,
    `sanitas_count` INT,
    `second_flatiron_count` INT,
    primary key (`id`)
) engine=InnoDB;