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

    functions = {
        "d": find_daily_stability,
        "w": find_weekly_stability,
        "m": find_monthly_stability,
        "a": find_annually_stability,
        "y": find_annually_stability,
    }

    if h not in functions:
        raise ValueError(
            "Invalid horizon. Use daily, weekly, monthly, or annual/yearly."
        )

    deliverables = functions[h](
        symbol=symbol,
        lookback=lookback,
        decay_parameter=decay_parameter,
        window_length=window_length,
    )

    relative_change = (
        float(deliverables["relative_volatility_change"]) * 100
    )

    if abs(relative_change) < 2:
        flag = "Smooth (Safe)"
    elif abs(relative_change) < 8:
        flag = "Moderate"
    else:
        flag = "High (Unsafe)"

    summary = {
        "symbol": symbol,
        "horizon": horizon,
        "volatility": {
            "raw": deliverables["volatility"],
            "percent": float(deliverables["volatility"]) * 100,
        },
        "time_weighted_volatility": {
            "raw": deliverables["time_weighted_volatility"],
            "percent": (
                float(deliverables["time_weighted_volatility"]) * 100
            ),
        },
        "volatility_uncertainty": {
            "raw": deliverables["volatility_dispersion"],
            "percent": (
                float(deliverables["volatility_dispersion"]) * 100
            ),
        },
        "relative_volatility_change": {
            "percent": relative_change,
            "flag": flag,
        },
    }

    if diagnostics:
        summary["temporal_smoothness_diagnostics"] = deliverables[
            "temporal_smoothness_diagnostics"
        ]

    return summary
