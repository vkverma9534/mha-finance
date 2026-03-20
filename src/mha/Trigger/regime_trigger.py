from mha.regimes.detection import (
    flag_weekly_regime,
    flag_monthly_regime,
    flag_annually_regime,
    flag_daily_regime
)

def volatility_trigger(
    symbol: str,
    horizon: str,
    lookback: int | None = None,
    window_length: int | None = None,
)-> dict:
    if horizon[0].lower() == "m":
        deliverables = flag_monthly_regime(symbol=symbol,
                                              lookback=lookback,
                                              window_length=window_length)
    elif horizon[0].lower() == "a" or horizon[0].lower() == "y":
        deliverables = flag_annually_regime(symbol=symbol,
                                              lookback=lookback,
                                              window_length=window_length)
    elif horizon[0].lower() == "w":
        deliverables = flag_weekly_regime(symbol=symbol,
                                              lookback=lookback,
                                              window_length=window_length)
    elif horizon[0].lower() == "d":
        deliverables = flag_daily_regime(symbol=symbol,
                                              lookback=lookback,
                                              window_length=window_length)
    else:
        raise ValueError("Invalid horizon")
    
    return deliverables