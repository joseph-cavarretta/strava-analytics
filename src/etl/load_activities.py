import os
import datetime
from dotenv import load_dotenv
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
PROCESSED_DATA_PATH = '../data/processed/'

TYPE_MAP = {}

def get_most_recent_file() -> str:
     last_file = os.listdir(PROCESSED_DATA_PATH)[-1]
     return PROCESSED_DATA_PATH + last_file


def get_mysql_creds() -> dict:
    """ Returns mysql connection object """
    return dict(
        user = os.getenv('mysql_username'),
        password = os.getenv('mysql_password'),
        host = os.getenv('mysql_host'),
        database = os.getenv('mysql_db')
    )


def mysql_insert_dataframe(df: pd.DataFrame, table: str) -> None:
    """ Inserts (appends) a pandas DataFrame """
    creds = get_mysql_creds()
    conn_string = f'mysql+mysqlconnector://{creds["user"]}:{creds["password"]}\
        @{creds["host"]}:{creds["port"]}/{creds["db"]}'
    eng = create_engine(conn_string, echo=False)
    df.to_sql(name=table, con=eng, if_exists='overwrite', index=False)
    print(f'{len(df)} rows inserted')


def load_fact_activities(df: pd.DataFrame) -> None:
    pass


def load_dim_date(df: pd.DataFrame) -> None:
    pass


def load_dim_type(df: pd.DataFrame) -> None:
    pass