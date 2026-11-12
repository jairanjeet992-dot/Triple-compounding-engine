from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    quantity: int
    max_loss: Decimal
    reason: str

def size_position(budget: Decimal, entry: Decimal, stop: Decimal,
                  estimated_cost_per_unit: Decimal = Decimal("0")) -> RiskDecision:
    if entry <= 0 or stop <= 0 or entry == stop or estimated_cost_per_unit < 0:
        return RiskDecision(False, 0, Decimal("0"), "Invalid inputs.")
    unit_risk = abs(entry - stop) + estimated_cost_per_unit
    if budget <= 0:
        return RiskDecision(False, 0, Decimal("0"), "No risk budget.")
    qty = int(budget // unit_risk)
    if qty < 1:
        return RiskDecision(False, 0, Decimal("0"), "Minimum unit exceeds risk budget.")
    return RiskDecision(True, qty, unit_risk * qty, "Within supplied risk budget.")
