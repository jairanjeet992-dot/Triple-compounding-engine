"""Performance statistics for research reports; frequency must be supplied explicitly."""
from __future__ import annotations

import math
import pandas as pd


def performance_metrics(equity: pd.Series, periods_per_year: int, risk_free_rate: float = 0.0) -> dict[str, float | int]:
    """Compute CAGR, annualised volatility, Sharpe and max drawdown.

    Returns are derived from the equity curve. CAGR is omitted as NaN when
    the series is too short or has non-positive endpoints. Sharpe uses the
    supplied annual risk-free rate and sample standard deviation.
    """
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    values = pd.to_numeric(equity, errors="coerce").dropna()
    if len(values) < 2 or (values <= 0).any():
        raise ValueError("equity must contain at least two positive observations")
    returns = values.pct_change().dropna()
    years = (len(returns) / periods_per_year)
    cagr = (values.iloc[-1] / values.iloc[0]) ** (1.0 / years) - 1.0 if years > 0 else float("nan")
    volatility = float(returns.std(ddof=1) * math.sqrt(periods_per_year)) if len(returns) > 1 else float("nan")
    periodic_rf = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = returns - periodic_rf
    std = excess.std(ddof=1)
    sharpe = float(excess.mean() / std * math.sqrt(periods_per_year)) if pd.notna(std) and std > 0 else float("nan")
    drawdown = values / values.cummax() - 1.0
    return {
        "observations": int(len(values)),
        "cagr": float(cagr),
        "annualized_volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": float(drawdown.min()),
    }


def compare_to_benchmark(strategy_equity: pd.Series, benchmark_close: pd.Series) -> pd.DataFrame:
    """Align strategy and benchmark returns on shared timestamps, without filling gaps."""
    if strategy_equity.index.has_duplicates or benchmark_close.index.has_duplicates:
        raise ValueError("duplicate timestamps are not allowed")
    strategy_returns = strategy_equity.sort_index().pct_change().rename("strategy_return")
    benchmark_returns = benchmark_close.sort_index().pct_change().rename("benchmark_return")
    aligned = pd.concat([strategy_returns, benchmark_returns], axis=1, join="inner").dropna()
    if aligned.empty:
        raise ValueError("strategy and benchmark have no overlapping return observations")
    return aligned
