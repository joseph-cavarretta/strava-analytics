import sys
import os
import datetime
import pandas as pd
import get_activities as strava

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
RAW_DATA_PATH = '../data/raw/'
OUT_PATH = f'../data/processed/processed_activities_{DATE}.csv'
METERS_TO_MILES = 0.000621371
METERS_TO_FEET = 3.28084
REFRESH = False


# if 'refresh' passed from CLI, call API to refresh activities before processing
if len(sys.argv) > 1:
     if sys.argv[1].lower() == 'refresh':
          REFRESH = True
     

def main():
     # add logger for pipeline
     data = load_data()
     process_dates(data)
     convert_units(data)
     save_processed_data(data)


def get_most_recent_file():
     last_file = os.listdir(RAW_DATA_PATH)[-1]
     return RAW_DATA_PATH + last_file


def load_data(refresh=REFRESH):
     if refresh:
          # refreshes all strava activities via API and saves them to strava_activities_raw.csv
          print("Refreshing activity data...")
          strava.main()
     data = get_most_recent_file()
     df = pd.read_csv(data)
     return df


def process_dates(df):
     df['start_date_local'] = pd.to_datetime(df['start_date_local'])
     df['day_of_month'] = df['start_date_local'].dt.day
     df['day_of_year'] = df['start_date_local'].dt.dayofyear
     df['week_of_year'] = df['start_date_local'].dt.strftime('%W') # gives week with Monday as first day of week
     df['month'] = df['start_date_local'].dt.month
     df['year'] = df['start_date_local'].dt.year
     df['date'] = df['start_date_local'].dt.date
     df['year_week'] = df['year'].astype(str) + '-' + df['week_of_year'].astype(str).str.zfill(2)


def convert_units(df):
     # convert distance to miles
     df['distance'] = (df['distance'] * METERS_TO_MILES).astype(float).round(2)
     # convert elevation gain to feet
     df['total_elevation_gain'] = (df['total_elevation_gain'] * METERS_TO_FEET).astype(float).round()
     # convert elapsed time (seconds) to hours
     df['hours'] = (df['elapsed_time'] / 60 / 60).round(2)
     df.rename(columns={'distance': 'miles', 'total_elevation_gain': 'elevation_gain'}, inplace=True)


def save_processed_data(df):
     df.to_csv(OUT_PATH, index=False)
     print('Data processed and file saved!')


if __name__ == '__main__':
     main()