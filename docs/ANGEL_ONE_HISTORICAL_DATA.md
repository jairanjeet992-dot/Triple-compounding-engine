# Angel One Historical Market Data

Angel One SmartAPI documents a historical candle endpoint:
`POST /rest/secure/angelbroking/historical/v1/getCandleData`.

Supported exchanges in the published documentation: NSE, NFO, BSE, BFO and MCX.
Supported intervals: 1, 3, 5, 10, 15 and 30 minutes, 1 hour and 1 day.

Documented maximum date span per request:
- 1 minute: 30 days
- 3 minutes: 60 days
- 5 minutes: 100 days
- 10 minutes: 100 days
- 15 minutes: 200 days
- 30 minutes: 200 days
- 1 hour: 400 days
- 1 day: 2,000 days

The provider must split larger history ranges into valid date windows and persist
results locally. The published per-request limits are not a promise of complete
historical availability for every instrument or token. Verify actual returned
coverage, missing sessions, volume conventions and symbol-token mapping.

The adapter added in this branch is a read-only HTTP integration layer. It
expects an authenticated httpx.Client from a future authentication module;
it does not log in, store API secrets, or place orders.

Before using research results, add:
- trading calendar and exchange holidays;
- instrument-master versioning and token mapping;
- corporate-action adjustments where appropriate;
- duplicate/missing candle detection and source provenance;
- date/segment-specific Indian transaction costs;
- data coverage reports and out-of-sample tests.

Official reference: https://smartapi.angelone.in/docs
