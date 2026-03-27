from typing import cast
from mha.volatility.daily_v import find_daily_stability
from mha.volatility.monthly_v import find_monthly_stability
from mha.volatility.weekly_v import find_weekly_stability
from mha.volatility.annually_v import find_annually_stability


def volatility_trigger(
    symbol: str,
    horizon: str,
    lookback: int | None = None,
    decay_parameter: float | None = None,
    window_length: int | None = None,
    diagnostics: bool = False,
) -> dict:
    if not horizon or not isinstance(horizon, str):
        raise ValueError("horizon must be a non-empty string")

    h = horizon.strip().lower()[0]

    if h == "m":
        deliverables = find_monthly_stability(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter,
            window_length=window_length,
        )

    elif h in {"a", "y"}:
        deliverables = find_annually_stability(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter,
            window_length=window_length,
        )

    elif h == "w":
        deliverables = find_weekly_stability(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter,
            window_length=window_length,
        )

    elif h == "d":
        deliverables = find_daily_stability(
            symbol=symbol,
            lookback=lookback,
            decay_parameter=decay_parameter,
            window_length=window_length,
        )

    else:
        raise ValueError(
            "Invalid horizon. Use daily, weekly, monthly, or annual/yearly."
        )

    cond_num = float(cast(int | float | str, deliverables["relative_volatility_change"])) * 100
    
    flag = (
        "Smooth (Safe)" if abs(cond_num) < 2
        else "Moderate" if abs(cond_num) < 8
        else "High (Unsafe)"
    )

    summary = {
        "symbol": symbol,
        "horizon": horizon,
        "volatility": {
            "raw": deliverables["volatility"],
            "percent": float(cast(int | float | str, deliverables["volatility"])) * 100,
        },
        "time_weighted_volatility": {
            "raw": deliverables["time_weighted_volatility"],
            "percent": float(cast(int | float | str, deliverables["time_weighted_volatility"])) * 100,
        },
        "volatility_uncertainty": {
            "raw": deliverables["volatility_dispersion"],
            "percent": float(cast(int | float | str, deliverables["volatility_dispersion"])) * 100,
        },
        "relative_volatility_change": {
            "percent": cond_num,
            "flag": flag,
        },
    }

    if diagnostics:
        summary["temporal_smoothness_diagnostics"] = deliverables[
            "temporal_smoothness_diagnostics"
        ]

    return summary