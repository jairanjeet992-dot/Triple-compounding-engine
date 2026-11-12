from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class CollateralStatus(str, Enum):
    VERIFIED = "verified"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class CollateralSnapshot:
    status: CollateralStatus
    broker_eligible_value: Decimal | None
    cash_component: Decimal | None
    non_cash_component: Decimal | None
    utilised_margin: Decimal | None
    fetched_age_seconds: int | None

@dataclass(frozen=True)
class DeployableCapacity:
    allowed: bool
    amount: Decimal
    reason: str

def calculate_deployable_capacity(snapshot: CollateralSnapshot,
                                  stress_buffer_pct: Decimal = Decimal("20")) -> DeployableCapacity:
    values = (snapshot.broker_eligible_value, snapshot.cash_component,
              snapshot.non_cash_component, snapshot.utilised_margin)
    if snapshot.status != CollateralStatus.VERIFIED or any(v is None for v in values):
        return DeployableCapacity(False, Decimal("0"), "Margin breakdown unknown or incomplete.")
    if snapshot.fetched_age_seconds is None or snapshot.fetched_age_seconds > 60:
        return DeployableCapacity(False, Decimal("0"), "Broker margin snapshot is stale.")
    if not (Decimal("0") <= stress_buffer_pct < Decimal("100")):
        return DeployableCapacity(False, Decimal("0"), "Invalid stress buffer.")
    # Conservative proxy: only broker-reported cash component; non-cash is not cash.
    # Final deployable margin must still be confirmed by broker/segment rules.
    gross = max(Decimal("0"), snapshot.cash_component - snapshot.utilised_margin)
    amount = gross * (Decimal("1") - stress_buffer_pct / Decimal("100"))
    return DeployableCapacity(True, amount, "Cash-component proxy only; broker segment checks remain mandatory.")
