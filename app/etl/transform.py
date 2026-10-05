from collections.abc import Sequence

import pandas as pd

from app.etl import schemas
from app.etl.models import CustomRoute

SECONDS_PER_HOUR = 3600


def process_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse start_date_local and derive all date dimension columns."""
    df = df.copy()
    df["start_date_local"] = pd.to_datetime(df["start_date_local"])
    df["day_of_month"] = df["start_date_local"].dt.day
    df["day_of_year"] = df["start_date_local"].dt.dayofyear
    df["week_of_year"] = df["start_date_local"].dt.strftime("%W")
    df["month"] = df["start_date_local"].dt.month
    df["year"] = df["start_date_local"].dt.year
    df["date"] = df["start_date_local"].dt.date
    df["year_week"] = (
        df["year"].astype(str) + "-" + df["week_of_year"].astype(str).str.zfill(2)
    )
    return df


def convert_units(
    df: pd.DataFrame, distance_conversion: float, elevation_conversion: float
) -> pd.DataFrame:
    """Convert distance and elevation by the given factors and add hours."""
    df = df.copy()
    df["distance"] = (df["distance"] * distance_conversion).astype(float).round(2)
    df["total_elevation_gain"] = (
        (df["total_elevation_gain"] * elevation_conversion).astype(float).round()
    )
    # elapsed_time is in seconds; hours is used for dashboard aggregations
    df["hours"] = (df["elapsed_time"] / SECONDS_PER_HOUR).round(2)
    return df.rename(
        columns={
            "distance": "miles",
            "moving_time": "moving_time_sec",
            "elapsed_time": "elapsed_time_sec",
            "total_elevation_gain": "elevation_gain_ft",
        }
    )


def _last_digit(names: pd.Series) -> pd.Series:
    """The repeat count written as the final character of an activity name."""
    return names.str.strip().str[-1].astype(int)


def count_custom_routes(
    df: pd.DataFrame, routes: Sequence[CustomRoute]
) -> pd.DataFrame:
    """Add a name and repeat-count column per route, read from activity names.

    "<route> x3" counts 3; any other name matching a route key counts 1; a name
    containing the route's repeat_key adds its trailing digit on top.
    """
    df = df.copy()
    for route in routes:
        df[route.name_col] = route.route_name
        df[route.count_col] = 0

        repeated = df.name.str.contains(f"{route.route_name} x", case=False, na=False)
        df.loc[repeated, route.count_col] = _last_digit(df.loc[repeated]["name"])

        single = (~repeated) & (
            df.name.str.contains("|".join(route.keys), case=False, na=False, regex=True)
        )
        df.loc[single, route.count_col] += 1

        if route.repeat_key is not None:
            has_repeat = df.name.str.contains(route.repeat_key, case=False, na=False)
            df.loc[has_repeat, route.count_col] += _last_digit(
                df.loc[has_repeat]["name"]
            )
    return df


def add_fk_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add foreign key columns for the type, date, and counts dimensions."""
    df = df.copy()
    labels = {val: key for key, lst in schemas.type_labels.items() for val in lst}
    df["label"] = df["type"].map(labels).fillna("omit")
    type_ids = {val: idx + 1 for idx, val in enumerate(df.type.unique())}
    df["type_id"] = df["type"].map(type_ids)
    df["date_id"] = df["date"].astype(str).str.replace("-", "")
    df["activity_id"] = df["id"]
    df["type_name"] = df["type"]
    return df


def transform(
    df: pd.DataFrame,
    distance_conversion: float,
    elevation_conversion: float,
    routes: Sequence[CustomRoute],
) -> pd.DataFrame:
    """Run every transformation and return the columns of the processed schema."""
    df = process_dates(df)
    df = convert_units(df, distance_conversion, elevation_conversion)
    df = count_custom_routes(df, routes)
    df = add_fk_columns(df)
    return df[schemas.processed_cols]
