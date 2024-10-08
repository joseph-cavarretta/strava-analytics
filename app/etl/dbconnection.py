import psycopg2 as pg
from psycopg2 import extras
from psycopg2 import sql
import yaml


class DbConnection:
    def __init__(self, config_path):
        self.conf_path = config_path
        self.config = self.__get_config()
        self.conn_string = self.__get_connection_string()
        self.conn = self.__connect()
        self.curs = self.__get_cursor()


    def __enter__(self):
        return self


    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.__close()


    def __get_config(self):
        with open(self.conf_path, 'r') as f:
            return yaml.safe_load(f)


    def __get_connection_string(self):
        user = self.config['db']['username']
        pw = self.config['db']['password']
        host = self.config['db']['host']
        port = self.config['db']['port']
        db_name = self.config['db']['database']
        return f'postgresql://{user}:{pw}@{host}:{port}/{db_name}'
    

    def __connect(self):
        return pg.connect(self.conn_string)


    def __get_cursor(self):
        return self.conn.cursor()


    def __close(self):
        # if error, implicit rollback() is called for uncommited changes
        self.conn.close()


    def __drop_table(self, table: str):
        queryText = f'TRUNCATE TABLE {table}'
        query = sql.SQL(queryText).format(table=sql.Identifier(table))
        self.curs.execute(query)


    def insert_multiple(self, table: str, records: list, columns: str):
        # using this syntax for inserts is faster 
        queryText = f"""INSERT INTO {table} ({columns}) VALUES %s"""
        query = sql.SQL(queryText).format(table=sql.Identifier(table))
        self.__drop_table(table)
        extras.execute_values(self.curs, query.as_string(self.curs), records)
        self.conn.commit()
