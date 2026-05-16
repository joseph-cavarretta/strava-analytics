import json
import logging
import time
import datetime
from pathlib import Path

import pandas as pd
import requests

from config import StravaSettings
from app.etl.schemas import raw_cols

logger = logging.getLogger(__name__)

DATE = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
OUT_PATH = Path(f"/app/data/raw/raw_activities_{DATE}.csv")


def main() -> None:
    """Fetch all Strava activities and write raw CSV to disk."""
    settings = StravaSettings()
    tokens = get_creds(settings)
    activities = get_activities(tokens)
    add_units_columns(activities)
    activities = order_columns(activities)
    save_file(activities)


def get_creds(settings: StravaSettings) -> dict:
    """Load OAuth tokens from the creds file, refreshing if expired.

    Args:
        settings: Strava API configuration with creds_path and secrets.

    Returns:
        Dict containing access_token, refresh_token, and expires_at.
    """
    logger.info("Getting API credentials.")
    with open(settings.creds_path) as f:
        tokens = json.load(f)
    if tokens["expires_at"] < time.time():
        tokens = refresh_tokens(tokens, settings)
    return tokens


def refresh_tokens(tokens: dict, settings: StravaSettings) -> dict:
    """Exchange a refresh token for a new access token via the Strava API.

    Args:
        tokens: Current token dict containing refresh_token.
        settings: Strava API configuration with client credentials.

    Returns:
        Updated token dict with new access_token and expires_at.
    """
    logger.info("Refreshing tokens...")
    response = requests.post(
        url="https://www.strava.com/oauth/token",
        data={
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
        },
    )
    new_tokens: dict = response.json()
    with open(settings.creds_path, "w") as f:
        json.dump(new_tokens, f)
    return new_tokens


def get_activities(tokens: dict) -> pd.DataFrame:
    """Fetch all activity pages from the Strava API.

    Args:
        tokens: Valid token dict containing access_token.

    Returns:
        DataFrame with one row per activity and the standard column set.
    """
    cols = [
        "id", "name", "start_date", "start_date_local", "type",
        "distance", "moving_time", "elapsed_time", "total_elevation_gain",
    ]
    activities = pd.DataFrame(columns=cols)
    page = 1
    url = "https://www.strava.com/api/v3/activities"

    logger.info("Getting activities from Strava. This may take a minute.")
    while True:
        r = requests.get(
            url,
            params={
                "access_token": tokens["access_token"],
                "per_page": 200,
                "page": page,
            },
        )
        records: list = r.json()
        if not records:
            break
        for i, record in enumerate(records):
            for col in cols:
                activities.loc[i + (page - 1) * 200, col] = record[col]
        page += 1

    logger.info("%d activities fetched.", len(activities))
    return activities


def add_units_columns(df: pd.DataFrame) -> None:
    """Annotate the DataFrame with unit label columns in place."""
    df["distance_units"] = "meters"
    df["elevation_units"] = "meters"
    df["time_units"] = "seconds"


def order_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return the DataFrame with columns reordered to the raw schema."""
    return df[raw_cols]


def save_file(df: pd.DataFrame) -> None:
    """Write the activities DataFrame to the raw output CSV path."""
    df.to_csv(OUT_PATH, index=False)
    logger.info("Activity refresh complete.")


if __name__ == "__main__":
    main()
