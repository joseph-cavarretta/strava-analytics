"""
Created on Mon Apr 5 23:19:28 2021
@author: joseph.cavarretta
"""
import sys
import pandas as pd
import numpy as np
import get_activities as strava

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
     get_bear_peak_counts(data)
     get_sanitas_counts(data)
     get_second_flatiron_counts(data)
     get_strength_counts(data)
     get_climbing_counts(data)
     save_processed_data(data)

def load_data(refresh=REFRESH):
     if refresh:
          # refreshes all strava activities via API and saves them to strava_activities_raw.csv
          print("Refreshing activity data...")
          strava.main()
     df = pd.read_csv('data/raw_activities.csv')
     return df


def process_dates(dataframe):
     df = dataframe
     df['start_date_local'] = pd.to_datetime(df['start_date_local'])
     df['day_of_month'] = df['start_date_local'].dt.day
     df['day_of_year'] = df['start_date_local'].dt.dayofyear
     df['week'] = df['start_date_local'].dt.strftime('%W') # gives week with Monday as first day of week
     df['month'] = df['start_date_local'].dt.month_name()
     df['year'] = df['start_date_local'].dt.year
     df['date'] = df['start_date_local'].dt.date
     df['year_week'] = df['year'].astype(str) + '-' + df['week'].astype(str).str.zfill(2)


def convert_units(dataframe):
     df = dataframe
     # convert distance to miles
     df['distance'] = (df['distance'] * METERS_TO_MILES).astype(float).round(2)
     # convert elevation gain to feet
     df['total_elevation_gain'] = (df['total_elevation_gain'] * METERS_TO_FEET).astype(float).round()
     # convert elapsed time (seconds) to hours
     df['hours'] = (df['elapsed_time'] / 60 / 60).round(2)
     df.rename(columns={'distance': 'miles', 'total_elevation_gain': 'elevation'}, inplace=True)


def get_session_rpe(dataframe):
     # perceived exertion not currently implemented in api
     # df = dataframe
     # df['session_load'] == (df['perceived_exertion'] * df['elapsed_time']) / 60
     pass


def get_bear_peak_counts(dataframe):
     df = dataframe
     key = 'bear peak'
     key_x = f'{key} x'
     col_name = 'bear_peak_count'
     # create new column and set values to 0
     df[col_name] = 0

     # if repeated summits, activity name is like 'bear peak x2'
     criteria_1 = df.name.str.contains(key_x, case=False, na=False)
     df.loc[criteria_1, col_name] = df.loc[criteria_1]['name'].str.strip().str[-1].astype(int)

     # otherwise one for each single summit labelled like 'bear peak' and skyline traverse which include bear peak
     criteria_2 = (((df.name.str.contains(key, case=False, na=False)) & 
                  (~df.name.str.contains(key_x, case=False, na=False))) |
                  (df.name.str.contains('skyline', case=False, na=False)))
     df.loc[criteria_2, col_name] = df.loc[criteria_2, col_name] = 1

     # if activity name includes 'summit repeat' add one additional for each summit repeat
     criteria_3 = df.name.str.contains('summit repeat', case=False, na=False)
     df.loc[criteria_3, col_name] += df.loc[criteria_3]['name'].str.strip().str[-1].astype(int)


def get_sanitas_counts(dataframe):
     df = dataframe
     key = 'sanitas'
     key_x = f'{key} x'
     col_name = 'sanitas_count'
     # create new column and set values to 0
     df[col_name] = 0

     # if repeated summits, activity name is like 'sanitas x2'
     criteria_1 = df.name.str.contains(key_x, case=False, na=False)
     df.loc[criteria_1, col_name] = df.loc[criteria_1]['name'].str.strip().str[-1].astype(int)

     # otherwise one for each single summit labelled like 'sanitas' and skyline traverse which include sanitas
     criteria_2 = (((df.name.str.contains(key, case=False, na=False)) & 
                  (~df.name.str.contains(key_x, case=False, na=False))) |
                  (df.name.str.contains('skyline', case=False, na=False)))
     df.loc[criteria_2, col_name] = df.loc[criteria_2, col_name] = 1


def get_second_flatiron_counts(dataframe):
     df = dataframe
     key = '2nd Flatiron'
     key_x = f'{key} x'
     col_name = 'second_flatiron_count'
     # check for alternate name and convert
     df['name'] = df['name'].str.replace('Freeway', '2nd Flatiron', case=False)
     # create new column and set values to 0
     df[col_name] = 0

     # if repeated summits, activity name is like '2nd flatiron x2'
     criteria_1 = df.name.str.contains(key_x, case=False, na=False)
     df.loc[criteria_1, col_name] = df.loc[criteria_1]['name'].str.strip().str[-1].astype(int)

     # otherwise one for each single summit labelled like '2nd flatiron'
     criteria_2 = ((df.name.str.contains(key, case=False, na=False)) & 
                  (~df.name.str.contains(key_x, case=False, na=False)))
     df.loc[criteria_2, col_name] = df.loc[criteria_2, col_name] = 1


def get_strength_counts(dataframe):
     df = dataframe
     df['strength_count'] = np.where((df['name'].str.contains('Strength', case=False, na=False)) & 
                                     (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['plyo_count'] = np.where((df['name'].str.contains('Plyo', case=False, na=False)) & 
                                  (df['type'].str.lower() == 'weighttraining'), 1, 0)


def get_climbing_counts(dataframe):
     df = dataframe
     df['indoor_climb_count'] = np.where((df['name'].str.contains('Climb', case=False, na=False))
                                       & (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['outdoor_climb_count'] = np.where((df['name'].str.contains('Climb', case=False, na=False))
                                        & (df['type'].str.lower() == 'rockclimbing'), 1, 0)

     df['indoor_boulder_count'] = np.where((df['name'].str.contains('Bouldering', case=False, na=False))
                                            & (df['type'].str.lower() == 'weighttraining'), 1, 0)

     df['outdoor_boulder_count'] = np.where((df['name'].str.contains('Bouldering', case=False, na=False))
                                             & (df['type'].str.lower() == 'rockclimbing'), 1, 0)


def get_skimo_count(dataframe):
     # type = backcountry ski
     pass

def get_climbing_grades(dataframe):
     # parse grades from description
     pass


def get_14ers_counts(dataframe):
     # new file with list of 14ers names
     pass


def save_processed_data(dataframe):
     df = dataframe
     df.to_csv('data/processed_activities.csv', index=False)
     print('Data processed and file saved!')


if __name__ == '__main__':
     main()