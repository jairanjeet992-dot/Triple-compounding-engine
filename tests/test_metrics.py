import pandas as pd
import pytest

from tce.backtesting.metrics import compare_to_benchmark, performance_metrics


def test_performance_metrics_report_drawdown_and_cagr():
    idx = pd.date_range("2025-01-01", periods=5, freq="D", tz="Asia/Kolkata")
    equity = pd.Series([100, 110, 105, 120, 125], index=idx)
    result = performance_metrics(equity, periods_per_year=252)
    assert result["observations"] == 5
    assert result["max_drawdown"] == pytest.approx(105 / 110 - 1)
    assert result["cagr"] > 0


def test_rejects_invalid_equity():
    with pytest.raises(ValueError):
        performance_metrics(pd.Series([100]), periods_per_year=252)


def test_benchmark_comparison_uses_only_shared_dates():
    idx = pd.date_range("2025-01-01", periods=4, freq="D", tz="Asia/Kolkata")
    strategy = pd.Series([100, 102, 101, 104], index=idx)
    benchmark = pd.Series([200, 201, 203], index=idx[1:])
    result = compare_to_benchmark(strategy, benchmark)
    assert list(result.columns) == ["strategy_return", "benchmark_return"]
    assert len(result) == 2


def test_rejects_duplicate_benchmark_timestamps():
    idx = pd.DatetimeIndex(["2025-01-01", "2025-01-01"], tz="Asia/Kolkata")
    with pytest.raises(ValueError, match="duplicate"):
        compare_to_benchmark(pd.Series([100, 101], index=idx), pd.Series([200, 201], index=idx))
