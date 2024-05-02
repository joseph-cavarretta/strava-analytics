-- to run: mysql -u root -p -e "source create_database.sql"

DROP DATABASE IF EXISTS `strava_staging`;

CREATE DATABASE IF NOT EXISTS `strava_staging`;
USE `strava_staging`;

CREATE TABLE IF NOT EXISTS `strava_staging`.`raw_data` (
    `id` INT NOT NULL, 
    `name` VARCHAR(99), 
    `start_date_local` VARCHAR(30), 
    `type` VARCHAR(30), 
    `distance` FLOAT(14,2), 
    `moving_time` int, 
    `elapsed_time` int, 
    `total_elevation_gain` FLOAT(14,2), 
    primary key (`id`)
) engine=InnoDB;

CREATE TABLE IF NOT EXISTS `strava_staging`.`processed_data` (
    `id` INT NOT NULL, 
    `name` VARCHAR(99), 
    `start_date_local` VARCHAR(30), 
    `type` VARCHAR(30), 
    `miles` FLOAT(6,2),
    `moving_time` INT,
    `elapsed_time` INT,
    `elevation` FLOAT(10,2),
    `day_of_month` INT,
    `day_of_year` INT,
    `week` INT,
    `month` INT,
    `year` INT,
    `bear_peak_count` INT,
    `sanitas_count` INT,
    `second_flatiron_count` INT,
    `strength_count` INT,
    `plyo_count` INT,
    `indoor_climb_count` INT,
    `outdoor_climb_count` INT,
    `indoor_boulder_count` INT,
    `outdoor_boulder_count` INT,
    primary key (`id`)
) engine=InnoDB;