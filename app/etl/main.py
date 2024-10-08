import sys
import datetime
from datahandler import DataHandler
from dbconnection import DbConnection
from schemas import (
    activity_cols, 
    date_cols, 
    type_cols, 
    counts_cols
)

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
DB_CONF = 'config.yml'
IN_PATH = '/app/data/raw/'
OUT_PATH = f'/app/data/processed/processed_activities_{DATE}.csv'
TABLES_PATH = f'/app/data/warehouse/{DATE}/'
METERS_TO_MILES = 0.000621371
METERS_TO_FEET = 3.28084
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

REFRESH = False

# if 'refresh' passed from CLI, call API to refresh activities before processing
if len(sys.argv) > 1:
     if sys.argv[1].lower() == 'refresh':
          REFRESH = True


def main():
    data = DataHandler(
        in_path = IN_PATH,
        processed_out_path = OUT_PATH,
        tables_out_path = TABLES_PATH,
        distance_conversion = METERS_TO_MILES,
        elevation_conversion = METERS_TO_FEET,
        custom_fields = CUSTOM_ROUTES,
        refresh = REFRESH
    )
    data.process()

    with DbConnection(DB_CONF) as db:
        for table, columns, key in [
        ['activities', activity_cols, 'id'],
        ['types', type_cols, 'type_id'],
        ['dates', date_cols, 'date_id'],
        ['counts', counts_cols, 'activity_id']
    ]:
            insert_params = data.get_table_data(
                table,
                columns,
                key
            )
            db.insert_multiple(
                insert_params.table,
                insert_params.records,
                insert_params.col_string
            )


if __name__ == '__main__':
    main()