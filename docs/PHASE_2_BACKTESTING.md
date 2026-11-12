# Phase 2 — Historical Data & Backtesting Foundation

## Scope in this branch
- Validate timezone-aware OHLCV candles; reject duplicates, missing values, impossible prices and negative volume.
- Run a deterministic long-only target-weight simulation.
- Signals are shifted one candle and filled at the next candle open to avoid same-bar look-ahead.
- Apply configurable fee and slippage basis points; report equity, cash, shares, turnover, costs, returns and drawdown.

## Explicit limitations
- This is a research primitive, not a validated strategy or production execution engine.
- No historical data provider is configured; no market data has been downloaded or verified.
- No taxes, exchange/broker charges, STT, GST, stamp duty, SEBI fees, DP charges, corporate actions, circuit limits, partial fills, liquidity/impact model or instrument lot-size rules are modelled yet. Results must not be treated as net tradable returns.
- Options, futures, BTST settlement, pledged collateral and Angel One execution are out of scope for this initial primitive.
- Paper/live trading remain disabled.

## Next validation gates
1. Select a licensed, reliable historical data source and document its adjustment/session conventions.
2. Add instrument master and corporate-action handling.
3. Implement complete India transaction-cost schedules by segment and date.
4. Add benchmark comparison, walk-forward/out-of-sample evaluation and survivorship-bias controls.
5. Add strategy-specific execution, liquidity, gap and risk models before any paper trading.
