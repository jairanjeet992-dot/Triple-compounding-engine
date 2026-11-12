from decimal import Decimal
from risk.collateral import CollateralSnapshot, CollateralStatus, calculate_deployable_capacity

def test_unknown_fails_closed():
    s = CollateralSnapshot(CollateralStatus.UNKNOWN, None, None, None, None, None)
    r = calculate_deployable_capacity(s)
    assert not r.allowed and r.amount == Decimal("0")

def test_stale_fails_closed():
    s = CollateralSnapshot(CollateralStatus.VERIFIED, Decimal("100000"), Decimal("60000"), Decimal("40000"), Decimal("10000"), 90)
    assert not calculate_deployable_capacity(s).allowed

def test_non_cash_not_counted_as_cash():
    s = CollateralSnapshot(CollateralStatus.VERIFIED, Decimal("100000"), Decimal("60000"), Decimal("40000"), Decimal("10000"), 5)
    r = calculate_deployable_capacity(s, Decimal("20"))
    assert r.allowed and r.amount == Decimal("40000")
