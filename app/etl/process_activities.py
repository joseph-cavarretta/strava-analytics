import sys
import os
import datetime
import pandas as pd
import numpy as np
import get_activities as strava
from schemas import processed_cols

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
RAW_DATA_PATH = '/app/data/raw/'
OUT_PATH = f'/app/data/processed/processed_activities_{DATE}.csv'
METERS_TO_MILES = 0.000621371
METERS_TO_FEET = 3.28084
REFRESH = False

CUSTOM_ROUTES = {
     1: {
          'name_col': 'route1_name',
          'count_col': 'route1_count',
          'route_name': 'bear peak',
          'keys': ['bear peak', 'skyline'],
          'repeat_key': 'summit repeat'
     },
     2: {
          'name_col': 'route2_name',
          'count_col': 'route2_count',
          'route_name': 'sanitas',
          'keys': ['sanitas', 'skyline']
     },
     3: {
          'name_col': 'route3_name',
          'count_col': 'route3_count',
          'route_name': '2nd flatiron',
          'keys': ['2nd flatiron', 'freeway']
     }
}

# if 'refresh' passed from CLI, call API to refresh activities before processing
if len(sys.argv) > 1:
     if sys.argv[1].lower() == 'refresh':
          REFRESH = True
     

def main():
     # TODO: add logger for pipeline
     data = load_data()
     process_dates(data)
     convert_units(data)
     for key in CUSTOM_ROUTES.keys():
          get_custom_route_counts(data, CUSTOM_ROUTES, key)
     data = order_columns(data)
     save_processed_data(data)


def get_most_recent_file() -> str:
     last_file = os.listdir(RAW_DATA_PATH)[-1]
     return RAW_DATA_PATH + last_file


def load_data(refresh=REFRESH):
     if refresh:
          # refreshes all strava activities from the API
          print("Refreshing activity data...")
          strava.main()
     data = get_most_recent_file()
     df = pd.read_csv(data)
     return df


def process_dates(df: pd.DataFrame) -> None:
     df['start_date_local'] = pd.to_datetime(df['start_date_local'])
     df['day_of_month'] = df['start_date_local'].dt.day
     df['day_of_year'] = df['start_date_local'].dt.dayofyear
     df['week_of_year'] = df['start_date_local'].dt.strftime('%W') # gives week with Monday as first day of week
     df['month'] = df['start_date_local'].dt.month
     df['year'] = df['start_date_local'].dt.year
     df['date'] = df['start_date_local'].dt.date
     df['year_week'] = df['year'].astype(str) + '-' + df['week_of_year'].astype(str).str.zfill(2)


def convert_units(df: pd.DataFrame) -> None:
     # convert distance to miles
     df['distance'] = (df['distance'] * METERS_TO_MILES).astype(float).round(2)
     # convert elevation gain to feet
     df['total_elevation_gain'] = (df['total_elevation_gain'] * METERS_TO_FEET).astype(float).round()
     # convert elapsed time (seconds) to hours
     df['hours'] = (df['elapsed_time'] / 60 / 60).round(2)
     df.rename(columns={
          'distance': 'miles', 
          'moving_time': 'moving_time_sec',
          'elapsed_time': 'elapsed_time_sec',
          'total_elevation_gain': 'elevation_gain_ft'
     }, inplace=True)


def get_custom_route_counts(df: pd.DataFrame, custom_routes_dict: dict, route_key: int):
     name_col = custom_routes_dict[route_key]['name_col']
     count_col = custom_routes_dict[route_key]['count_col']
     route_name = custom_routes_dict[route_key]['route_name']
     route_name_x = f'{route_name} x'
     keys = custom_routes_dict[route_key]['keys']
     # add new col with route name
     df[name_col] = route_name
     # create new column and set values to 0
     df[count_col] = 0

     # if repeated route, activity name is like '{key} x2'
     criteria_1 = df.name.str.contains(route_name_x, case=False, na=False)
     df.loc[criteria_1, count_col] = df.loc[criteria_1]['name'].str.strip().str[-1].astype(int)

     # otherwise one for each single route labelled with any keys in keys list
     criteria_2 = ((~df.name.str.contains(route_name_x, case=False, na=False)) &
            df.name.str.contains('|'.join(keys), case=False, na=False, regex=True))
     df.loc[criteria_2, count_col] = df.loc[criteria_2, count_col] + 1

     if 'repeat_key' in custom_routes_dict[route_key]:
          repeat_key = custom_routes_dict[route_key]['repeat_key']
          # if activity name includes special repeat_key add one additional for each 
          # will be listed like 'bear peak + summit repeat x3, which equals 4 summits
          criteria_3 = df.name.str.contains(repeat_key, case=False, na=False)
          df.loc[criteria_3, count_col] += df.loc[criteria_3]['name'].str.strip().str[-1].astype(int)


def get_strength_counts(df):
     df['strength_count'] = np.where((df['name'].str.contains('Strength', case=False, na=False)) & 
                                     (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['plyo_count'] = np.where((df['name'].str.contains('Plyo', case=False, na=False)) & 
                                  (df['type'].str.lower() == 'weighttraining'), 1, 0)


def get_climbing_counts(df):
     df['indoor_climb_count'] = np.where((df['name'].str.contains('Climb', case=False, na=False))
                                       & (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['outdoor_climb_count'] = np.where((df['name'].str.contains('Climb', case=False, na=False))
                                        & (df['type'].str.lower() == 'rockclimbing'), 1, 0)

     df['indoor_boulder_count'] = np.where((df['name'].str.contains('Bouldering', case=False, na=False))
                                            & (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['outdoor_boulder_count'] = np.where((df['name'].str.contains('Bouldering', case=False, na=False))
                                             & (df['type'].str.lower() == 'rockclimbing'), 1, 0)


def get_climbing_grades(df):
     # parse grades from description
     pass


def get_14ers_counts(df):
     # new file with list of 14ers names
     pass


def order_columns(df):
    return df[processed_cols]


def save_processed_data(df):
     df.to_csv(OUT_PATH, index=False)
     print('Data processed and file saved!')


if __name__ == '__main__':
     main()