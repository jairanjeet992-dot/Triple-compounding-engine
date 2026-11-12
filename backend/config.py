from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    trading_mode: str = "paper"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./tce_dev.db"
    max_daily_loss_pct: float = 0.50
    max_portfolio_drawdown_pct: float = 5.00
    max_risk_per_trade_pct: float = 0.25
    collateral_stress_buffer_pct: float = 20.00
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
