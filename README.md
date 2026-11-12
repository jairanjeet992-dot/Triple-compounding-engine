# Triple Compounding Engine (TCE)

Research-first portfolio and trading system for an Indian Angel One account.

## Three portfolio sleeves
1. ETF wealth sleeve — investments, allocation, P&L and rebalancing.
2. Equity intraday sleeve — scanner, entry/exit, sizing, charges and reconciliation.
3. BTST/overnight sleeve — gap-risk, settlement and corporate-action controls.

The requested 12% annual return per sleeve is an aspiration, not a forecast or guarantee. It must never become a trade quota or cause larger positions. Report sleeve and combined returns, volatility, drawdown, profit factor, costs and collateral usage.

## Current status
Phase 0 foundation has been added. Angel One is **not connected**. This repository currently has a read-only adapter boundary, not a working login. No live order placement is implemented.

## Non-negotiable safety
- Research/paper mode only by default.
- Fail closed: stale data, missing margin fields, unknown instrument mapping, API errors or unreconciled positions mean NO TRADE.
- Use broker-reported cash/non-cash margin, eligible collateral value, haircut, utilised margin, blocked funds, orders and positions. Never infer usable cash from ETF market value.
- LiquidBeES and Nippon India Liquid Fund must be classified from Angel One's actual eligibility and cash/non-cash margin treatment. Never hard-code assumptions.
- Pledged collateral can be revalued and haircuts/margin requirements can change. Maintain stress buffers.
- Risk sizing includes stop distance, charges and slippage, plus daily and portfolio loss limits.
- Options are out of initial scope pending a dedicated derivatives risk model.

## Local setup
Python 3.11+:
```bash
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
pytest -q
```
Keep real credentials only in local secrets or a managed secret store. Never commit them.

## Build sequence
1. Verify current official Angel One SmartAPI docs, authentication, account permissions and static-IP/API requirements.
2. Implement read-only authentication, funds/margin, holdings, positions and open orders.
3. Add data feeds, instrument master and reconciliation.
4. Build and validate separate ETF, intraday and BTST backtests with realistic costs.
5. Run paper trading and performance attribution.
6. Consider live execution only after compliance/security review and explicit approval.

See `docs/` for the blueprint, architecture, security baseline and integration plan.

Not investment advice. Trading and pledged-collateral strategies can lose money due to gaps, slippage, liquidity, margin changes or broker square-off. No return is guaranteed.
