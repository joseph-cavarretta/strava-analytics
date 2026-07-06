from typing import Any

from pydantic import BaseModel, ConfigDict


class TableInsertParams(BaseModel):
    """Parameters for a single bulk table insert."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    table: str
    records: list[Any]
    col_string: str


class RouteConfig(BaseModel):
    """Configuration for deriving repeat counts of a named route."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    name_col: str
    count_col: str
    route_name: str
    keys: list[str]
    repeat_key: str | None = None
