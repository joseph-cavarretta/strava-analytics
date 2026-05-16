import logging
from pathlib import Path

import pandas as pd

from app.etl import get_activities as strava
from app.etl.models import TableInsertParams
import app.etl.schemas as schemas

logger = logging.getLogger(__name__)


class DataHandler:
    """Orchestrates loading, transforming, and staging Strava activity data."""

    def __init__(
        self,
        in_path: Path,
        processed_out_path: Path,
        tables_out_path: Path,
        distance_conversion: float = 1.0,
        elevation_conversion: float = 1.0,
        custom_fields: dict | None = None,
        refresh: bool = False,
    ) -> None:
        self.in_path = in_path
        self.processed_out_path = processed_out_path
        self.tables_out_path = tables_out_path
        self.distance_conversion = distance_conversion
        self.elevation_conversion = elevation_conversion
        self.custom_fields = custom_fields or {}
        self.refresh = refresh
        self.data = self._get_dataframe()

    def _get_dataframe(self) -> pd.DataFrame:
        """Load activities from disk, refreshing from the API if requested."""
        if self.refresh:
            logger.info("Refreshing activity data from Strava API...")
            strava.main()
        path = self._get_most_recent_file()
        return pd.read_csv(path)

    def _get_most_recent_file(self) -> Path:
        """Return the most recently written raw activity file."""
        files = sorted(self.in_path.iterdir())
        return files[-1]

    def _process_dates(self) -> None:
        """Parse start_date_local and derive all date dimension columns."""
        self.data["start_date_local"] = pd.to_datetime(self.data["start_date_local"])
        self.data["day_of_month"] = self.data["start_date_local"].dt.day
        self.data["day_of_year"] = self.data["start_date_local"].dt.dayofyear
        self.data["week_of_year"] = self.data["start_date_local"].dt.strftime("%W")
        self.data["month"] = self.data["start_date_local"].dt.month
        self.data["year"] = self.data["start_date_local"].dt.year
        self.data["date"] = self.data["start_date_local"].dt.date
        self.data["year_week"] = (
            self.data["year"].astype(str)
            + "-"
            + self.data["week_of_year"].astype(str).str.zfill(2)
        )

    def _convert_units(self) -> None:
        """Convert distance to miles, elevation to feet, and time to hours."""
        self.data["distance"] = (
            self.data["distance"] * self.distance_conversion
        ).astype(float).round(2)
        self.data["total_elevation_gain"] = (
            self.data["total_elevation_gain"] * self.elevation_conversion
        ).astype(float).round()
        # elapsed_time is in seconds; hours is used for dashboard aggregations
        self.data["hours"] = (self.data["elapsed_time"] / 3600).round(2)
        self.data.rename(
            columns={
                "distance": "miles",
                "moving_time": "moving_time_sec",
                "elapsed_time": "elapsed_time_sec",
                "total_elevation_gain": "elevation_gain_ft",
            },
            inplace=True,
        )

    def _get_custom_route_counts(self) -> None:
        """Derive per-route repeat counts from activity name patterns."""
        for key in self.custom_fields:
            name_col = self.custom_fields[key]["name_col"]
            count_col = self.custom_fields[key]["count_col"]
            route_name = self.custom_fields[key]["route_name"]
            route_name_x = f"{route_name} x"
            keys = self.custom_fields[key]["keys"]

            self.data[name_col] = route_name
            self.data[count_col] = 0

            repeated = self.data.name.str.contains(route_name_x, case=False, na=False)
            self.data.loc[repeated, count_col] = (
                self.data.loc[repeated]["name"].str.strip().str[-1].astype(int)
            )

            single = (~repeated) & (
                self.data.name.str.contains("|".join(keys), case=False, na=False, regex=True)
            )
            self.data.loc[single, count_col] += 1

            if "repeat_key" in self.custom_fields[key]:
                repeat_key = self.custom_fields[key]["repeat_key"]
                has_repeat = self.data.name.str.contains(repeat_key, case=False, na=False)
                self.data.loc[has_repeat, count_col] += (
                    self.data.loc[has_repeat]["name"].str.strip().str[-1].astype(int)
                )

    def _add_fk_columns(self) -> None:
        """Add foreign key columns for the type, date, and counts dimensions."""
        labels_d = {
            val: key for key, lst in schemas.type_labels.items() for val in lst
        }
        self.data["label"] = self.data["type"].map(labels_d).fillna("omit")
        types_d = {
            val: idx + 1 for idx, val in enumerate(self.data.type.unique())
        }
        self.data["type_id"] = self.data["type"].map(types_d)
        self.data["date_id"] = self.data["date"].astype(str).str.replace("-", "")
        self.data["activity_id"] = self.data["id"]
        self.data["type_name"] = self.data["type"]

    def _order_columns(self) -> None:
        """Reorder columns to match the processed schema."""
        self.data = self.data[schemas.processed_cols]

    def _save_processed_data(self) -> None:
        """Write the fully processed DataFrame to the configured output path."""
        self.data.to_csv(self.processed_out_path, index=False)
        logger.info("Data processed and saved to %s.", self.processed_out_path)

    def _save_table_file(self, data: pd.DataFrame, filename: str) -> None:
        """Write a dimension table slice to the warehouse output directory."""
        self.tables_out_path.mkdir(parents=True, exist_ok=True)
        data.to_csv(self.tables_out_path / filename, index=False)

    def process(self) -> None:
        """Run the full transformation pipeline."""
        self._process_dates()
        self._convert_units()
        self._get_custom_route_counts()
        self._add_fk_columns()
        self._order_columns()
        self._save_processed_data()

    def get_table_data(
        self, table: str, columns: list[str], sort_key: str
    ) -> TableInsertParams:
        """Extract and stage a dimension table for database insertion.

        Args:
            table: Target table name.
            columns: Column subset to extract.
            sort_key: Column to sort by before inserting.

        Returns:
            TableInsertParams with table name, records, and column string.
        """
        data = self.data.loc[:, columns].drop_duplicates().sort_values(by=sort_key)
        records = data.to_records(index=False).tolist()
        col_string = ",".join(columns)
        self._save_table_file(data, f"{table}.csv")
        return TableInsertParams(table=table, records=records, col_string=col_string)
