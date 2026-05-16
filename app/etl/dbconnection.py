import logging
from types import TracebackType
from typing import Any

import psycopg2 as pg
from psycopg2 import extras, sql

from config import DatabaseSettings

logger = logging.getLogger(__name__)


class DbConnection:
    """Context manager wrapping a psycopg2 connection for bulk inserts."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self.settings = settings
        self.conn = pg.connect(settings.url)
        self.curs = self.conn.cursor()

    def __enter__(self) -> "DbConnection":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.conn.close()

    def _truncate(self, table: str) -> None:
        """Truncate a table before re-inserting all records."""
        query = sql.SQL("TRUNCATE TABLE {table}").format(table=sql.Identifier(table))
        self.curs.execute(query)

    def insert_multiple(self, table: str, records: list[Any], columns: str) -> None:
        """Truncate the table and bulk-insert all records.

        Args:
            table: Target table name.
            records: List of tuples to insert.
            columns: Comma-separated column names matching the record tuples.
        """
        query = sql.SQL(f"INSERT INTO {table} ({columns}) VALUES %s").format(
            table=sql.Identifier(table)
        )
        self._truncate(table)
        extras.execute_values(self.curs, query.as_string(self.curs), records)
        self.conn.commit()
        logger.info("Inserted %d records into %s.", len(records), table)
