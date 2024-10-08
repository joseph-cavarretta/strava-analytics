import os
from collections import namedtuple
import pandas as pd
import schemas
import get_activities as strava


class DataHandler:
    def __init__(self, 
                 in_path: str = None,
                 processed_out_path: str = None,
                 tables_out_path: str = None,
                 distance_conversion: float = 1,
                 elevation_conversion: float = 1,
                 custom_fields: dict = None,
                 refresh: bool = False

    ):
        self.in_path = in_path
        self.processed_out_path = processed_out_path
        self.tables_out_path = tables_out_path
        self.distance_conversion = distance_conversion
        self.elevation_conversion = elevation_conversion
        self.custom_fields = custom_fields
        self.refresh = refresh
        self.data = self.__get_dataframe()


    def __get_dataframe(self) -> pd.DataFrame:
        if self.refresh:
            # refreshes all strava activities from the API
            print("Refreshing activity data...")
            strava.main()
        data = self.__get_most_recent_file()
        return pd.read_csv(data)


    def __get_most_recent_file(self) -> str:
        last_file = os.listdir(self.in_path)[-1]
        return self.in_path + last_file


    def __process_dates(self) -> None:
        self.data['start_date_local'] = pd.to_datetime(self.data['start_date_local'])
        self.data['day_of_month'] = self.data['start_date_local'].dt.day
        self.data['day_of_year'] = self.data['start_date_local'].dt.dayofyear
        # gives week with Monday as first day of week
        self.data['week_of_year'] = self.data['start_date_local'].dt.strftime('%W')
        self.data['month'] = self.data['start_date_local'].dt.month
        self.data['year'] = self.data['start_date_local'].dt.year
        self.data['date'] = self.data['start_date_local'].dt.date
        self.data['year_week'] = self.data['year'].astype(str) + '-' \
            + self.data['week_of_year'].astype(str).str.zfill(2)


    def __convert_units(self) -> None:
        # convert distance to miles
        self.data['distance'] = (
             self.data['distance'] * self.distance_conversion
        ).astype(float).round(2)
        # convert elevation gain to feet
        self.data['total_elevation_gain'] = (
             self.data['total_elevation_gain'] * self.elevation_conversion
        ).astype(float).round()
        # convert elapsed time (seconds) to hours
        self.data['hours'] = (self.data['elapsed_time'] / 60 / 60).round(2)
        self.data.rename(columns={
            'distance': 'miles', 
            'moving_time': 'moving_time_sec',
            'elapsed_time': 'elapsed_time_sec',
            'total_elevation_gain': 'elevation_gain_ft'
        }, inplace=True)


    def __get_custom_route_counts(self) -> None:
        for key in self.custom_fields:
            name_col = self.custom_fields[key]['name_col']
            count_col = self.custom_fields[key]['count_col']
            route_name = self.custom_fields[key]['route_name']
            route_name_x = f'{route_name} x'
            keys = self.custom_fields[key]['keys']
            # add new col with route name
            self.data[name_col] = route_name
            # create new column and set values to 0
            self.data[count_col] = 0

            # if repeated route, activity name is like '{key} x2'
            criteria_1 = self.data.name.str.contains(
                route_name_x, case=False, na=False
            )
            self.data.loc[criteria_1, count_col] = \
                self.data.loc[criteria_1]['name'].str.strip().str[-1].astype(int)

            # otherwise one for each single route labelled with any keys in keys list
            criteria_2 = (
                (~self.data.name.str.contains(route_name_x, case=False, na=False)) 
                &
                (self.data.name.str.contains('|'.join(keys), case=False, na=False, regex=True))
            )
            self.data.loc[criteria_2, count_col] = \
                self.data.loc[criteria_2, count_col] + 1

            if 'repeat_key' in self.custom_fields[key]:
                repeat_key = self.custom_fields[key]['repeat_key']
                # if activity name includes special repeat_key add one additional for each 
                # will be listed like 'bear peak + summit repeat x3, which equals 4 summits
                criteria_3 = self.data.name.str.contains(
                    repeat_key, case=False, na=False
                )
                self.data.loc[criteria_3, count_col] += \
                    self.data.loc[criteria_3]['name'].str.strip().str[-1].astype(int)
     

    def __add_fk_columns(self) -> None:
        # flatten type_labels dict to map to self.data values
        labels_d = {
            val:key for key, lst in schemas.type_labels.items() for val in lst
        }
        self.data['label'] = self.data['type'].map(labels_d)
        # fill remaining values with 'omit'
        self.data['label'] = self.data['label'].fillna('omit')
        # create a map of unique ints for each activity type
        types_d = {
            val:idx+1 for idx, val in enumerate(self.data.type.unique())
        }
        self.data['type_id'] = self.data['type'].map(types_d)
        # date id is just the date field with no "-"
        self.data['date_id'] = self.data['date'].astype(str).str.replace('-', '')
        # activity_id is needed as FK in counts table
        self.data['activity_id'] = self.data['id']
        self.data['type_name'] = self.data['type']


    def __order_columns(self):
        self.data = self.data[schemas.processed_cols]


    def __save_processed_data(self) -> None:
        self.data.to_csv(self.processed_out_path, index=False)
        print('Data processed and file saved!')


    def __save_table_file(self, data: pd.DataFrame, filename: str) -> None:
        if not os.path.isdir(self.tables_out_path):
            os.mkdir(self.tables_out_path)
        data.to_csv(self.tables_out_path + filename, index=False)


    @staticmethod
    def __columns_string(columns: list) -> str:
        return ','.join(columns)

    @staticmethod
    def __records(data: pd.DataFrame) -> list:
        return data.to_records(index=False).tolist()
    

    def process(self) -> None:
        self.__process_dates()
        self.__convert_units()
        self.__get_custom_route_counts()
        self.__add_fk_columns()
        self.__order_columns()
        self.__save_processed_data()


    def get_table_data(self, table: str, columns: list, sort_key: str) -> tuple:
        data = self.data.loc[:, columns].drop_duplicates().sort_values(by=sort_key)
        records = self.__records(data)
        col_str = self.__columns_string(columns)
        self.__save_table_file(data, f'{table}.csv')
        Params = namedtuple('Params', ['table', 'records', 'col_string'])
        return Params(table, records, col_str)