from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class BrokerResult:
    ok: bool
    fetched_at: datetime
    data: dict[str, Any] | None = None
    error_code: str | None = None
    message: str | None = None

class AngelOneReadOnlyAdapter:
    """Fail-closed boundary; no login or order placement is implemented yet.

    Implement only against the verified current official SmartAPI contract.
    Keep credentials server-side and never add order placement to this class.
    """
    def __init__(self, client: Any | None = None):
        self._client = client

    @property
    def connected(self) -> bool:
        return self._client is not None

    def account_snapshot(self) -> BrokerResult:
        if self._client is None:
            return BrokerResult(False, datetime.now(timezone.utc), error_code="NOT_CONFIGURED",
                                message="Not configured; no broker request was made.")
        raise NotImplementedError("Read-only endpoint mapping awaits official SmartAPI verification.")
