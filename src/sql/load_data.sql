-- to run: mysql -u root -p -e "source load_data.sql"
-- mysql --local_infile=1 -u root -p -e "source load_data.sql"

LOAD DATA LOCAL INFILE "data/raw_activities.csv"
INTO TABLE `strava`.`raw`
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE "data/processed_activities.csv"
INTO TABLE `strava`.`processed`
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;