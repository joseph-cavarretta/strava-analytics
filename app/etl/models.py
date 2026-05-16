from typing import Any

from pydantic import BaseModel, ConfigDict


class TableInsertParams(BaseModel):
    """Parameters for a single bulk table insert."""

    model_config = ConfigDict(frozen=True)

    table: str
    records: list[Any]
    col_string: str
