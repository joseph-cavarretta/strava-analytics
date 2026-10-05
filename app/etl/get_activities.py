import json
import logging
import time
from pathlib import Path

import pandas as pd
import requests

from app.etl.models import StravaTokens
from app.etl.schemas import raw_cols
from config import StravaSettings

logger = logging.getLogger(__name__)

OAUTH_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities"
PAGE_SIZE = 200
REQUEST_TIMEOUT_SECONDS = 30
ACTIVITY_COLS = [
    "id",
    "name",
    "start_date",
    "start_date_local",
    "type",
    "distance",
    "moving_time",
    "elapsed_time",
    "total_elevation_gain",
]


def fetch_activities(settings: StravaSettings, out_path: Path) -> None:
    """Fetch all Strava activities and write the raw CSV to out_path."""
    tokens = get_creds(settings)
    activities = get_activities(tokens)
    add_units_columns(activities)
    order_columns(activities).to_csv(out_path, index=False)
    logger.info("Activity refresh complete.")


def get_creds(settings: StravaSettings) -> StravaTokens:
    """Load OAuth tokens from the creds file, refreshing them if expired."""
    logger.info("Getting API credentials.")
    with settings.creds_path.open() as f:
        tokens = StravaTokens.model_validate(json.load(f))
    if tokens.expires_at < time.time():
        tokens = refresh_tokens(tokens, settings)
    return tokens


def refresh_tokens(tokens: StravaTokens, settings: StravaSettings) -> StravaTokens:
    """Exchange the refresh token for new tokens and save Strava's whole response."""
    logger.info("Refreshing tokens...")
    response = requests.post(
        url=OAUTH_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
        data={
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": tokens.refresh_token,
        },
    )
    payload = response.json()
    with settings.creds_path.open("w") as f:
        json.dump(payload, f)
    return StravaTokens.model_validate(payload)


def get_activities(tokens: StravaTokens) -> pd.DataFrame:
    """Fetch every page of activities, one row per activity."""
    activities = pd.DataFrame(columns=ACTIVITY_COLS)
    page = 1
    logger.info("Getting activities from Strava. This may take a minute.")
    while True:
        params: dict[str, str | int] = {
            "access_token": tokens.access_token,
            "per_page": PAGE_SIZE,
            "page": page,
        }
        response = requests.get(
            ACTIVITIES_URL, timeout=REQUEST_TIMEOUT_SECONDS, params=params
        )
        records = response.json()
        if not records:
            break
        for i, record in enumerate(records):
            for col in ACTIVITY_COLS:
                activities.loc[i + (page - 1) * PAGE_SIZE, col] = record[col]
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
