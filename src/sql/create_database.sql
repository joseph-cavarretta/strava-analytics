-- to run: mysql -u root -p -e "source create_database.sql"

DROP DATABASE IF EXISTS `activities`;

CREATE DATABASE `activities`;
USE `activities`;

CREATE TABLE `activities`.`raw` (
    `id` INT NOT NULL, 
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
    `elevation_units` VARCHAR(10),
    PRIMARY KEY (`id`)
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
    PRIMARY KEY (`id`)
) engine=InnoDB;

CREATE TABLE `activities`.`activity` (
    `id` INT NOT NULL, 
    `date_id` DATE NOT NULL,
    `type_id` INT NOT NULL,
    `name` VARCHAR(99),
    `miles` FLOAT(6,2),
    `hours` FLOAT(10,2),
    `moving_time_sec` INT,
    `elapsed_time_sec` INT,
    `elevation_gain_ft` FLOAT(10,2),
    PRIMARY KEY (`id`)
) engine=InnoDB;


CREATE TABLE `activities`.`type` (
    `type_id` INT NOT NULL,
    `name` VARCHAR(99),
    PRIMARY KEY (`type_id`)
) engine=InnoDB;


CREATE TABLE `activities`.`date` (
    `date_id` DATE NOT NULL,
    `type_id` INT NOT NULL,
    `name` VARCHAR(99),
    PRIMARY KEY (`date_id`)
) engine=InnoDB;


CREATE TABLE `activities`.`counts` (
    `activity_id` INT NOT NULL,
    `route1_name` VARCHAR(20),
    `route1_count` INT,
    `route2_name` VARCHAR(20),
    `route2_count` INT,
    `route3_name` VARCHAR(20),
    `route3_count` INT,
    PRIMARY KEY (`activity_id`)
) engine=InnoDB;