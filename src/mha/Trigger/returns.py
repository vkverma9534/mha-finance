from mha.returns.daily import find_daily_estimations
from mha.returns.monthly import find_monthly_estimations
from mha.returns.weekly import find_weekly_estimations
from mha.returns.annually import find_annaul_estimations

def returns_trigger(symbol: str,
                    horizon: str,
                    lookback:int|None=None,
                    decay_parameter:float|None=None)-> dict:
    if horizon[0].lower() == "m":
        deliverables=find_monthly_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if horizon[0].lower() == "a" or horizon[0].lower() == "y":
        deliverables=find_annaul_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if horizon=="w":
        deliverables=find_weekly_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if horizon=="d":
        deliverables=find_daily_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
        
    
    horizon_map = {
        "M": "Monthly",
        "A": "Annual",
        "W": "Weekly",
        "D": "Daily",
    }

    result = {
        "symbol": symbol,
        "horizon": horizon_map.get(horizon, "Unknown"),
        "mean_returns_pct": deliverables[0] * 100,
        "median_returns_pct": deliverables[1] * 100,
        "time_weighted_mean_returns_pct": deliverables[2] * 100,
        "dispersion_pct": deliverables[3] * 100,
    }
    
    return result
    