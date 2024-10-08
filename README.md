## Overview
This project exports all of a users activities from the Strava REST API, transforms the data to generate custom metrics, and models the data into an interactive web dashboard using the Dash library for Flask within a Docker container.

**Note:** This project does not currently accept API tokens for other users. A future version will allow users to inject their own API crednetials to dashboard their own data.

<p align="center">
<img width='1400' alt='Dashboard' src='https://user-images.githubusercontent.com/57957983/226228269-63b9c991-44ad-478c-ac8a-7a7041cda3e7.png'>
</p>


## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)


## Run App
Run the following commands in your terminal from the root project directory:
```
chmod +x scripts/build.sh
chmod +x scripts/run.sh
```
Make sure your Docker Daemon is running, and then run the following:
```
source scripts/build.sh
source scripts/run.sh
```
Visit localhost http://0.0.0.0:8050/ in your browser to view data

## Load MySQL
To load processed data into a local MySQL database instance:  
Make sure you have MySQL running locally and run the following commands in yur terminal
```
mysql -u root -p -e "source create_database.sql"
mysql --local_infile=1 -u root -p -e "source load_data.sql"
```

## Developed by:
Joseph Cavarretta |
joseph.m.cavarretta@gmail.com |
[Github](https://github.com/joseph-cavarretta) |
[LinkedIn](https://www.linkedin.com/in/joseph-cavarretta-87242871/)
