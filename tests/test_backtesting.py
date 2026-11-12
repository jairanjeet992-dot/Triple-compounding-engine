import pandas as pd
import pytest

from tce.backtesting.data import validate_ohlcv
from tce.backtesting.engine import BacktestConfig, run_backtest


def sample_data():
    idx = pd.date_range("2026-01-01", periods=3, freq="D", tz="Asia/Kolkata")
    return pd.DataFrame({"open":[100, 101, 102], "high":[102, 103, 104],
                         "low":[99, 100, 101], "close":[101, 102, 103],
                         "volume":[1000, 1100, 1200]}, index=idx)


def test_validation_returns_sorted_copy():
    data = sample_data().iloc[::-1]
    validated = validate_ohlcv(data)
    assert validated.index.is_monotonic_increasing
    assert data.index.is_monotonic_decreasing


def test_rejects_naive_timestamps():
    data = sample_data()
    data.index = data.index.tz_localize(None)
    with pytest.raises(ValueError, match="timezone-aware"):
        validate_ohlcv(data)


def test_signal_executes_on_next_bar_and_costs_reduce_equity():
    data = sample_data()
    weights = pd.Series([1.0, 1.0, 1.0], index=data.index)
    result = run_backtest(data, weights, BacktestConfig(fee_bps=10, slippage_bps=10))
    assert result.iloc[0]["shares"] == 0
    assert result.iloc[1]["shares"] > 0
    assert result["costs"].sum() > 0


def test_rejects_invalid_weights():
    data = sample_data()
    weights = pd.Series([0.0, 1.2, 0.0], index=data.index)
    with pytest.raises(ValueError, match="between 0 and 1"):
        run_backtest(data, weights)
