# Product Blueprint

TCE is a personal research, risk and execution-control system for an Indian Angel One account.

## Three sleeves
1. ETF wealth sleeve: holdings, allocation, P&L and rebalancing.
2. Equity intraday sleeve: scanner, entry/exit, sizing, charges and reconciliation.
3. BTST sleeve: overnight equity positions with gap-risk, settlement and corporate-action controls.

Options are out of scope initially. Add only after a separate derivatives risk model for lot sizes, expiry, volatility, liquidity, spreads and margin.

## Central collateral manager
Read broker-reported available funds and the cash/non-cash margin breakdown, eligible collateral value, haircut, utilised margin, blocked amounts, orders and positions. Never infer usable cash from ETF market value. Treat LiquidBeES and Nippon India Liquid Fund using the broker's actual eligibility and cash/non-cash classifications, not assumptions. Unknown or stale margin data means NO TRADE.

## Return objectives
The requested 12% annual return per sleeve is an aspiration, not a forecast or guarantee. It must never become a trade quota or cause larger positions. Report sleeve and combined returns, volatility, drawdown, profit factor, costs, collateral utilisation and benchmark comparison.

## Modes
Research -> Paper -> Read-only broker -> (future, separately approved live mode). Live execution is not implemented.
