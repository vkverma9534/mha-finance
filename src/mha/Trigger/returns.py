from mha.returns.daily import find_daily_estimations
from mha.returns.monthly import find_monthly_estimations
from mha.returns.weekly import find_weekly_estimations
from mha.returns.annually import find_annaul_estimations

def returns_trigger(symbol: str,
                    horizon: str,
                    lookback:int|None=None,
                    decay_parameter:float|None=None)-> dict:
    
    h = horizon[0].lower()

    if h == "m":
        deliverables = find_monthly_estimations(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter
        )

    elif h in ("a", "y"):
        deliverables = find_annaul_estimations(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter
        )

    elif h == "w":
        deliverables = find_weekly_estimations(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter
        )

    elif h == "d":
        deliverables = find_daily_estimations(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter
        )

    else:
        raise ValueError("Invalid horizon")

    horizon_map = {
        "m": "Monthly",
        "a": "Annual",
        "y": "Annual",
        "w": "Weekly",
        "d": "Daily",
    }

    result = {
        "symbol": symbol,
        "horizon": horizon_map[h],
        "mean_returns_pct": deliverables[0] * 100,
        "median_returns_pct": deliverables[1] * 100,
        "time_weighted_mean_returns_pct": deliverables[2] * 100,
        "dispersion_pct": deliverables[3] * 100,
    }

    return result
