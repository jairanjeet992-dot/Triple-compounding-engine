from datetime import datetime, timedelta

import pytest

from tce.providers.angel_one_historical import build_candle_payload, parse_candle_response


def test_build_payload_accepts_documented_interval_and_timezone():
    start = datetime(2026, 1, 1, 9, 15, tzinfo=__import__("zoneinfo").ZoneInfo("Asia/Kolkata"))
    payload = build_candle_payload("NSE", "3045", "FIVE_MINUTE", start, start + timedelta(days=10))
    assert payload["symboltoken"] == "3045"
    assert payload["interval"] == "FIVE_MINUTE"


def test_rejects_window_over_documented_limit():
    start = datetime(2026, 1, 1, tzinfo=__import__("zoneinfo").ZoneInfo("Asia/Kolkata"))
    with pytest.raises(ValueError, match="100-day"):
        build_candle_payload("NSE", "3045", "FIVE_MINUTE", start, start + timedelta(days=101))


def test_parses_candle_response_to_india_timezone():
    result = parse_candle_response({"status": True, "data": [["2026-01-01T09:15:00+05:30", 100, 102, 99, 101, 500]]})
    assert str(result.index.tz) == "Asia/Kolkata"
    assert result.iloc[0]["close"] == 101


def test_rejects_unsuccessful_response():
    with pytest.raises(RuntimeError, match="failed"):
        parse_candle_response({"status": False, "message": "bad token"})
