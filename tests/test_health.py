from backend.main import health

def test_health_is_paper_only():
    result = health()
    assert result["status"] == "ok"
    assert result["trading_mode"] == "paper"
    assert result["live_orders_enabled"] is False
