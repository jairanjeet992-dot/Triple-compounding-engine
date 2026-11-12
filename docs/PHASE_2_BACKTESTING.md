# Phase 2 — Historical Data & Backtesting Foundation

## Implemented in this branch
- Validate timezone-aware OHLCV candles; reject duplicates, missing values, impossible prices and negative volume.
- Run a deterministic long-only target-weight simulation.
- Signals are shifted one candle and filled at the next candle open to avoid same-bar look-ahead.
- Apply configurable fee and slippage basis points; report equity, cash, shares, turnover, costs, returns and drawdown.
- Calculate CAGR, annualised volatility, Sharpe ratio and maximum drawdown with explicit observations-per-year input.
- Align strategy and benchmark returns only on shared timestamps; missing dates are not forward-filled.

## Explicit limitations
- Research primitives only; no strategy has been validated and no historical market data has been downloaded or verified.
- No data provider is configured. Provider selection must account for licensing, timestamp/session conventions, corporate-action adjustments and data quality.
- Costs are generic fee/slippage basis points, not a complete India schedule. STT, GST, stamp duty, exchange/broker fees, SEBI fees, DP charges and date/segment-specific rules are not yet modelled.
- No taxes, corporate actions, circuit limits, partial fills, liquidity/market impact, instrument lot-size rules, survivorship-bias controls or walk-forward validation yet.
- Options, futures, BTST settlement, pledged collateral and Angel One execution are out of scope for this foundation.
- Paper/live trading remain disabled.

## Next validation gates
1. Choose a licensed historical data source and document its adjustment/session conventions.
2. Add instrument master, trading calendar and corporate-action handling.
3. Implement date- and segment-specific Indian transaction costs.
4. Add benchmark datasets, walk-forward/out-of-sample evaluation and survivorship-bias controls.
5. Add strategy-specific execution, liquidity, gap and risk models before paper trading.
