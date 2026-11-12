# Architecture

Angel One read-only adapter -> normalised timestamped account snapshot -> collateral/risk engine -> market data -> independent strategy engines -> backtester/paper broker -> audit ledger -> dashboard.

## Boundaries
- BrokerAdapter: broker authentication and normalised reads only.
- AccountSnapshot: funds, margin breakup, holdings, positions and orders with provenance and timestamp.
- CollateralEngine: eligibility, haircut, cash/non-cash split, stress buffer and deployable capacity.
- Strategy interface: deterministic signals from validated data; no broker access.
- RiskEngine: sleeve, instrument, daily and portfolio limits.
- ExecutionGateway: paper-only initially.
- AuditLog: input snapshot, strategy version, risk outcome and simulated fills.

## Fail closed
Reject stale/incomplete account snapshots, invalid candles, un-reconciled positions and ambiguous order state. Use idempotency keys; never blindly retry non-idempotent orders. Circuit-break on repeated API failures, data disconnects or loss-limit breach.
