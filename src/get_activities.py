"""
Created on Mon Apr 5 23:19:28 2021
@author: joseph.cavarretta
"""
import pandas as pd
import requests
import json
import time
import configparser
from pathlib import Path

CONFIG_PATH = Path('config/strava_API.config')
CREDS_PATH = Path('config/strava_tokens.json')
OUT_PATH = Path('data/raw_activities.csv')


def main():
    tokens = get_creds()
    activities = get_activities(tokens)
    save_file(activities)


def get_creds():
    print('Getting API credentials.')
    with open(CREDS_PATH) as json_file:
        strava_tokens = json.load(json_file)

    # if access_token has expired then use the refresh_tokens to get the new one
    if strava_tokens['expires_at'] < time.time():
        # make Strava auth API call with current refresh token
        strava_tokens = refresh_tokens(strava_tokens)
    return strava_tokens


def refresh_tokens(strava_tokens):
    print('Refreshing strava tokens...')
    my_config_parser = configparser.ConfigParser()
    my_config_parser.read(CONFIG_PATH)
    client_id = my_config_parser.get('DEFAULT', 'client_id')
    client_secret = my_config_parser.get('DEFAULT', 'client_secret')
    response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                        'client_id': f'{client_id}',
                        'client_secret': f'{client_secret}',
                        'grant_type': 'refresh_token',
                        'refresh_token': strava_tokens['refresh_token']
                    }
    )
    new_strava_tokens = response.json()
    # save new tokens to file
    with open(CREDS_PATH, 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
    return new_strava_tokens


def get_activities(strava_tokens):
    # loop through all activities
    page = 1
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']

    # create the dataframe ready for the API call to store your activity data
    cols = [
        'id', 'name', 'start_date_local', 'type', 'distance', 
        'moving_time', 'elapsed_time', 'total_elevation_gain'
    ]
    activities = pd.DataFrame(columns=cols)

    print('Getting activities from strava. This may take a minute.')
    while True:
        # get page of activities from Strava
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        # if no results then exit loop
        if (not r):
            break

        # add data to dataframe
        for x in range(len(r)):
            for col in cols:
              activities.loc[x + (page-1)*200, col] = r[x][col]  
        # increment page
        page += 1

    print(f'{len(activities)} activities fetched.')
    return activities


def save_file(dataframe):
    dataframe.to_csv(OUT_PATH, index=False)
    print ('Activities refreshed!')

if __name__ == '__main__':
    main()