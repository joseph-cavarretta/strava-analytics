import datetime
import logging
import sys

from app.etl.datahandler import DataHandler
from app.etl.dbconnection import DbConnection
from app.etl.get_activities import fetch_activities
from app.etl.models import CustomRoute
from app.etl.schemas import activity_cols, counts_cols, date_cols, type_cols
from config import get_settings

logger = logging.getLogger(__name__)

METERS_TO_MILES = 0.000621371
METERS_TO_FEET = 3.28084
CUSTOM_ROUTES = (
    CustomRoute(
        name_col="route1_name",
        count_col="route1_count",
        route_name="bear peak",
        keys=["bear peak", "skyline"],
        repeat_key="summit repeat",
    ),
    CustomRoute(
        name_col="route2_name",
        count_col="route2_count",
        route_name="sanitas",
        keys=["sanitas", "skyline"],
    ),
    CustomRoute(
        name_col="route3_name",
        count_col="route3_count",
        route_name="2nd flatiron",
        keys=["2nd flatiron", "freeway"],
    ),
)


def main() -> None:
    """Run the full ETL pipeline: extract, transform, and load into Postgres."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    settings = get_settings()
    date = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

    if len(sys.argv) > 1 and sys.argv[1].lower() == "refresh":
        logger.info("Refreshing activity data from Strava API...")
        fetch_activities(
            settings.strava, settings.data_in_path / f"raw_activities_{date}.csv"
        )

    data = DataHandler(
        in_path=settings.data_in_path,
        processed_out_path=settings.data_out_path / f"processed_activities_{date}.csv",
        tables_out_path=settings.tables_out_path / date,
        distance_conversion=METERS_TO_MILES,
        elevation_conversion=METERS_TO_FEET,
        custom_routes=CUSTOM_ROUTES,
    )
    data.process()

    with DbConnection(settings.db) as db:
        for table, columns, key in [
            ("activities", activity_cols, "id"),
            ("types", type_cols, "type_id"),
            ("dates", date_cols, "date_id"),
            ("counts", counts_cols, "activity_id"),
        ]:
            params = data.get_table_data(table, columns, key)
            db.insert_multiple(params.table, params.records, params.col_string)


if __name__ == "__main__":
    main()
