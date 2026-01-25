import numpy as np
import math
from typing import List
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter1d
import pandas as pd
from datetime import datetime, timezone, timedelta


def volatility_trigger(
    symbol: str,
    horizon: str,
    lookback: float | None = None,
    decay_parameter: float | None = None,
    window_length: float | None = None,
    diagnostics: bool = False
):
    if horizon == "M":
        deliverables = find_monthly_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    elif horizon == "A":
        deliverables = find_annaully_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    elif horizon == "W":
        deliverables = find_weekly_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    elif horizon == "D":
        deliverables = find_daily_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    else:
        raise ValueError("Invalid horizon")

    print(f"Symbol: {symbol}")
    print(f"Horizon: {horizon}")

    print(f"Volatility of Returns: {deliverables['volatility']*100:.2f}%")
    print(f"Time Weighted Volatility: {deliverables['time_weighted_volatility']*100:.2f}%")
    print(f"Volatility Uncertainty: {deliverables['volatility_dispersion']*100:.2f}%")

    cond_num = deliverables["relative_volatility_change"] * 100
    flag = (
        "Smooth (Safe)" if abs(cond_num) < 2
        else "Moderate" if abs(cond_num) < 8
        else "High (Unsafe)"
    )

    print(f"Relative Volatility Change: {cond_num:.2f}% → {flag}")

    if diagnostics:
        print("Temporal Smoothness Diagnostics:")
        print("  • Interactive Plotly figure")
        deliverables["temporal_smoothness_diagnostics"].show()

    return deliverables
