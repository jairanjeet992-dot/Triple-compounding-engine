"""Angel One SmartAPI historical candle adapter.

Authentication is supplied by the caller; this module never stores credentials.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
import pandas as pd

HISTORICAL_CANDLE_URL = (
    "https://apiconnect.angelone.in/rest/secure/angelbroking/"
    "historical/v1/getCandleData"
)

INTERVAL_MAX_DAYS = {
    "ONE_MINUTE": 30,
    "THREE_MINUTE": 60,
    "FIVE_MINUTE": 100,
    "TEN_MINUTE": 100,
    "FIFTEEN_MINUTE": 200,
    "THIRTY_MINUTE": 200,
    "ONE_HOUR": 400,
    "ONE_DAY": 2000,
}

SUPPORTED_EXCHANGES = {"NSE", "NFO", "BSE", "BFO", "MCX"}


class AngelOneHistoricalDataError(RuntimeError):
    """Raised when Angel One returns an invalid or unsuccessful response."""


def build_candle_payload(
    exchange: str,
    symbol_token: str,
    interval: str,
    fromdate: datetime,
    todate: datetime,
) -> dict[str, str]:
    exchange = exchange.upper()
    if exchange not in SUPPORTED_EXCHANGES:
        raise ValueError(f"Unsupported exchange: {exchange}")
    if interval not in INTERVAL_MAX_DAYS:
        raise ValueError(f"Unsupported interval: {interval}")
    if not symbol_token or not symbol_token.isdigit():
        raise ValueError("symbol_token must be a numeric instrument token")
    if fromdate.tzinfo is None or todate.tzinfo is None:
        raise ValueError("fromdate and todate must be timezone-aware")
    if todate <= fromdate:
        raise ValueError("todate must be later than fromdate")
    max_days = INTERVAL_MAX_DAYS[interval]
    if (todate - fromdate).total_seconds() > max_days * 86400:
        raise ValueError(f"{interval} request exceeds documented {max_days}-day window")
    return {
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "fromdate": fromdate.strftime("%Y-%m-%d %H:%M"),
        "todate": todate.strftime("%Y-%m-%d %H:%M"),
    }


def parse_candle_response(payload: dict[str, Any]) -> pd.DataFrame:
    if payload.get("status") is not True:
        raise AngelOneHistoricalDataError(
            f"Angel One historical API failed: {payload.get('message', 'unknown error')}"
        )
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise AngelOneHistoricalDataError("Historical response data is not a list")
    if not rows:
        return pd.DataFrame(
            columns=["open", "high", "low", "close", "volume"],
            index=pd.DatetimeIndex([], tz="Asia/Kolkata", name="timestamp"),
        )
    try:
        frame = pd.DataFrame(
            rows, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).dt.tz_convert(
            "Asia/Kolkata"
        )
        frame = frame.set_index("timestamp")
        for column in ["open", "high", "low", "close", "volume"]:
            frame[column] = pd.to_numeric(frame[column], errors="raise")
        return frame
    except (TypeError, ValueError, KeyError) as exc:
        raise AngelOneHistoricalDataError("Malformed historical candle response") from exc


class AngelOneHistoricalDataProvider:
    """Thin read-only adapter. Pass an authenticated httpx.Client from auth layer."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def fetch_candles(
        self,
        exchange: str,
        symbol_token: str,
        interval: str,
        fromdate: datetime,
        todate: datetime,
    ) -> pd.DataFrame:
        body = build_candle_payload(exchange, symbol_token, interval, fromdate, todate)
        response = self._client.post(HISTORICAL_CANDLE_URL, json=body, timeout=20.0)
        response.raise_for_status()
        return parse_candle_response(response.json())
