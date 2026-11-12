# Angel One SmartAPI Integration Plan

Status: NOT CONNECTED. This is a plan, not a working integration.

Before coding, verify current official SmartAPI SDK/docs, authentication flow, session lifetime, app permissions, static-IP/API access prerequisites, applicable retail-algo requirements, read endpoints, rate limits and market-data terms.

First scope is read-only: session health, profile, funds/limits and margin breakup, holdings, positions and open orders. Normalise responses into timestamped schemas. Keep redacted fixtures for tests. Do not infer cash collateral or eligible pledge value from holdings value.

Never ask for or commit the user's PIN, TOTP seed, API key or access token. Use local environment or a secret manager.

Acceptance: valid session reads only expected endpoints; expired session fails closed; missing margin fields become UNKNOWN; rate-limit/network failures back off and trigger a circuit breaker; logs are credential-free.
