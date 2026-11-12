from fastapi import FastAPI

app = FastAPI(title="Triple Compounding Engine", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "trading_mode": "paper", "live_orders_enabled": False}
