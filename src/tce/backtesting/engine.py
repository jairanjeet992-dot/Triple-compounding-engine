"""Small, deterministic long-only backtester with next-bar execution and costs."""
from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .data import validate_ohlcv


@dataclass(frozen=True)
class BacktestConfig:
    initial_cash: float = 100_000.0
    fee_bps: float = 5.0
    slippage_bps: float = 5.0

    def __post_init__(self) -> None:
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be positive")
        if self.fee_bps < 0 or self.slippage_bps < 0:
            raise ValueError("fees and slippage cannot be negative")


def run_backtest(candles: pd.DataFrame, target_position: pd.Series, config: BacktestConfig = BacktestConfig()) -> pd.DataFrame:
    """Execute target weights at the next candle open; weights must be 0..1.

    The supplied signal at row t is deliberately shifted to t+1 to avoid
    same-candle look-ahead. This is a research primitive, not a live strategy.
    """
    data = validate_ohlcv(candles)
    if not target_position.index.equals(data.index):
        raise ValueError("target_position index must exactly match candle index")
    if target_position.isna().any() or ((target_position < 0) | (target_position > 1)).any():
        raise ValueError("target weights must be non-null and between 0 and 1")

    weights = target_position.astype(float).shift(1).fillna(0.0)
    cash = float(config.initial_cash)
    shares = 0.0
    rows: list[dict[str, float | pd.Timestamp]] = []
    cost_rate = (config.fee_bps + config.slippage_bps) / 10_000.0

    for timestamp, candle in data.iterrows():
        price = float(candle["open"])
        desired_value = cash + shares * price
        desired_shares = (desired_value * float(weights.loc[timestamp])) / price
        delta = desired_shares - shares
        traded_value = abs(delta) * price
        costs = traded_value * cost_rate
        cash -= delta * price + costs
        shares = desired_shares
        equity = cash + shares * float(candle["close"])
        rows.append({"timestamp": timestamp, "cash": cash, "shares": shares,
                     "equity": equity, "traded_value": traded_value, "costs": costs})

    result = pd.DataFrame(rows).set_index("timestamp")
    result["return"] = result["equity"].pct_change().fillna(0.0)
    result["drawdown"] = result["equity"] / result["equity"].cummax() - 1.0
    return result
