import os
import datetime
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

DATE = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
PROCESSED_DATA_PATH = '../data/processed/'
OUT_PATH = f'../data/warehouse/{DATE}/'


def get_most_recent_file() -> str:
     last_file = os.listdir(PROCESSED_DATA_PATH)[-1]
     return PROCESSED_DATA_PATH + last_file


def save_file(df: pd.DataFrame, filename: str) -> None:
    pass


def mysql_connect() -> dict:
    """ Returns mysql connection object """
    return mysql.connector.connect(
        user = os.getenv('mysql_username'),
        password = os.getenv('mysql_password'),
        host = os.getenv('mysql_host'),
        database = os.getenv('mysql_db')
    )


def mysql_insert_multiple(query: str, data: list) -> None:
    """ Inserts multiple rows to table """
    with mysql_connect() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()
        print(f'{cursor.rowcount} rows inserted')


def load_fact_activities(df: pd.DataFrame) -> None:
    pass


def load_dim_date(df: pd.DataFrame) -> None:
    pass


def load_dim_type(df: pd.DataFrame) -> None:
    pass