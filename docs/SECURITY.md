# Security Baseline

- Keep secrets in local environment or a managed secret store, never in GitHub, code, issues, logs or chat.
- Treat API keys, PIN, TOTP seed and access tokens as highly sensitive; rotate if exposed.
- Broker credentials and tokens stay server-side, never in browser JavaScript.
- Encrypt persisted tokens and account data; restrict database access.
- Redact credentials and auth headers from logs and exceptions.
- HTTPS only for remote deployment; protect sessions, cookies and CSRF.
- Pin dependencies and scan for vulnerabilities.
- Audit login, account reads, config changes and trade approvals.
- Live execution remains disabled pending separate review.
