from pydantic import BaseModel, ConfigDict


class TableInsertParams(BaseModel):
    """Parameters for a single bulk table insert."""

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)

    table: str
    records: list[tuple[object, ...]]
    col_string: str


class StravaTokens(BaseModel):
    """The OAuth fields this pipeline reads from Strava's token response."""

    # Strava's token response carries more (athlete, token_type, ...); the creds file
    # keeps the whole response, and only these fields are read back.
    model_config = ConfigDict(extra="ignore", frozen=True)

    access_token: str
    refresh_token: str
    expires_at: int


class CustomRoute(BaseModel):
    """A named route whose repeats are counted from activity names."""

    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)

    name_col: str
    count_col: str
    route_name: str
    keys: list[str]
    repeat_key: str | None = None
