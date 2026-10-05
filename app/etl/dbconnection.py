import logging
from collections.abc import Sequence
from types import TracebackType

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

    def insert_multiple(
        self, table: str, records: Sequence[tuple[object, ...]], columns: str
    ) -> None:
        """Replace the table's contents with records.

        columns is a comma-separated list naming the fields of each record tuple, in
        order. The table is truncated first, so this is a full reload, not an append.
        """
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES %s").format(
            table=sql.Identifier(table),
            columns=sql.SQL(", ").join(
                sql.Identifier(col) for col in columns.split(",")
            ),
        )
        self._truncate(table)
        extras.execute_values(self.curs, query.as_string(self.curs), records)
        self.conn.commit()
        logger.info("Inserted %d records into %s.", len(records), table)
