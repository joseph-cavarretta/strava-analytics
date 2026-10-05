import logging
from collections.abc import Sequence
from pathlib import Path

import pandas as pd

from app.etl.models import CustomRoute, TableInsertParams
from app.etl.transform import transform

logger = logging.getLogger(__name__)


class DataHandler:
    """Loads raw Strava activities, transforms them, and stages the output files."""

    def __init__(
        self,
        in_path: Path,
        processed_out_path: Path,
        tables_out_path: Path,
        distance_conversion: float = 1.0,
        elevation_conversion: float = 1.0,
        custom_routes: Sequence[CustomRoute] = (),
    ) -> None:
        self.in_path = in_path
        self.processed_out_path = processed_out_path
        self.tables_out_path = tables_out_path
        self.distance_conversion = distance_conversion
        self.elevation_conversion = elevation_conversion
        self.custom_routes = custom_routes
        self.data = pd.read_csv(self._get_most_recent_file())

    def _get_most_recent_file(self) -> Path:
        """Return the most recently written raw activity file."""
        files = sorted(self.in_path.iterdir())
        return files[-1]

    def _save_table_file(self, data: pd.DataFrame, filename: str) -> None:
        """Write a dimension table slice to the warehouse output directory."""
        self.tables_out_path.mkdir(parents=True, exist_ok=True)
        data.to_csv(self.tables_out_path / filename, index=False)

    def process(self) -> None:
        """Run the full transformation pipeline and save the processed file."""
        self.data = transform(
            self.data,
            self.distance_conversion,
            self.elevation_conversion,
            self.custom_routes,
        )
        self.data.to_csv(self.processed_out_path, index=False)
        logger.info("Data processed and saved to %s.", self.processed_out_path)

    def get_table_data(
        self, table: str, columns: list[str], sort_key: str
    ) -> TableInsertParams:
        """Save the deduplicated `columns` of the data, sorted, and stage the insert."""
        data = self.data.loc[:, columns].drop_duplicates().sort_values(by=sort_key)
        records = data.to_records(index=False).tolist()
        self._save_table_file(data, f"{table}.csv")
        return TableInsertParams(
            table=table, records=records, col_string=",".join(columns)
        )
