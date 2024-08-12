import os
import datetime
from dotenv import load_dotenv
import sqlalchemy as sa
import psycopg2 as pg
from psycopg2 import extras
from psycopg2 import sql
import pandas as pd
from schemas import (
    activity_cols, 
    date_cols, 
    type_cols, 
    counts_cols,
    type_labels
)

load_dotenv()

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
PROCESSED_DATA_PATH = '/app/data/processed/'
OUT_PATH = f'/app/data/warehouse/{DATE}/'


def get_most_recent_file() -> str:
     last_file = os.listdir(PROCESSED_DATA_PATH)[0]
     return PROCESSED_DATA_PATH + last_file


def read_file() -> pd.DataFrame:
    return pd.read_csv(get_most_recent_file())


def add_fk_columns(df: pd.DataFrame) -> None:
    # flatten type_labels dict to map to df values
    labels_d = {val:key for key, lst in type_labels.items() for val in lst}
    df['label'] = df['type'].map(labels_d)
    # fill remaining values with 'omit'
    df['label'] = df['label'].fillna('omit')
    # create a map of unique ints for each activity type
    types_d = {val:idx+1 for idx, val in enumerate(df.type.unique())}
    df['type_id'] = df['type'].map(types_d)
    # date id is just the date field with no "-"
    df['date_id'] = df['date'].str.replace('-', '')
    # activity_id is needed as FK in counts table
    df['activity_id'] = df['id']
    df['type_name'] = df['type']

def get_psql_conn_string():
    user = os.getenv('pg_user')
    pw = os.getenv('pg_pw')
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    db_name = os.getenv('pg_db_name')
    return f'postgresql://{user}:{pw}@{host}:{port}/{db_name}'


def psql_connect():
    """ Returns psql connection object """
    conn_string = get_psql_conn_string()
    return pg.connect(conn_string)


def psql_drop_table(cursor, table):
    queryText = f'TRUNCATE TABLE {table}'
    query = sql.SQL(queryText).format(table=sql.Identifier(table))
    cursor.execute(query)
    
def psql_insert_multiple(data: list, table: str, columns: str) -> None:
    """ Inserts list of rows to table """
    conn = psql_connect()
    cursor = conn.cursor()
    queryText = f'INSERT INTO {table} ({columns}) VALUES %s'
    query = sql.SQL(queryText).format(table=sql.Identifier(table))

    try:
        psql_drop_table(cursor, table)
        extras.execute_values(cursor, query.as_string(cursor), data)
    except Exception as err:
        conn.rollback()
        raise err
    else:
        conn.commit()
        print(f'Insert query to {table} successful')
    finally:
         conn.close()


def save_file(df: pd.DataFrame, filename: str) -> None:
    if not os.path.isdir(OUT_PATH):
        os.mkdir(OUT_PATH)
    df.to_csv(OUT_PATH+filename, index=False)


def load_table(df: pd.DataFrame, table: str, columns: list, sort_key: str) -> None:
    data = df.loc[:, columns].drop_duplicates().sort_values(by=sort_key)
    records = data.to_records(index=False).tolist()
    col_str = ','.join(columns)
    psql_insert_multiple(records, table, col_str)
    save_file(data, f'{table}.csv')
    

if __name__ == '__main__':
    df = read_file()
    add_fk_columns(df)
    for table, columns, key in [
        ['activities', activity_cols, 'id'],
        ['types', type_cols, 'type_id'],
        ['dates', date_cols, 'date_id'],
        ['counts', counts_cols, 'activity_id']
    ]:
        load_table(df, table, columns, key)