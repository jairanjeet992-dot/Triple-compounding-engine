"""Historical OHLCV input validation for the research pipeline."""
from __future__ import annotations

import pandas as pd

REQUIRED = ("open", "high", "low", "close", "volume")


def validate_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted, validated copy; reject ambiguous or unsafe market data."""
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise ValueError("OHLCV index must be a DatetimeIndex")
    if frame.index.tz is None:
        raise ValueError("OHLCV timestamps must be timezone-aware")
    if frame.empty:
        raise ValueError("OHLCV data is empty")
    if frame.index.has_duplicates:
        raise ValueError("Duplicate candle timestamps are not allowed")
    missing = [column for column in REQUIRED if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing OHLCV columns: {', '.join(missing)}")

    result = frame.loc[:, REQUIRED].copy().sort_index()
    if result[list(REQUIRED)].isna().any().any():
        raise ValueError("OHLCV data contains missing values")
    if (result[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("OHLC prices must be positive")
    if (result["volume"] < 0).any():
        raise ValueError("Volume cannot be negative")
    invalid_range = (result["high"] < result[["open", "close", "low"]].max(axis=1)) | (result["low"] > result[["open", "close", "high"]].min(axis=1))
    if invalid_range.any():
        raise ValueError("OHLC candle high/low range is inconsistent")
    return result
