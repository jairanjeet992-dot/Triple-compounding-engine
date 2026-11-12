from decimal import Decimal
from risk.limits import size_position

def test_position_size_respects_budget():
    r = size_position(Decimal("250"), Decimal("100"), Decimal("95"))
    assert r.allowed and r.quantity == 50 and r.max_loss == Decimal("250")

def test_invalid_stop_rejected():
    assert not size_position(Decimal("250"), Decimal("100"), Decimal("100")).allowed
