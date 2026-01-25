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


def diagnostics(log_returns: np.ndarray,
                window_length: int|None=None) -> go.Figure:
    if window_length==None:
        window_length=len(log_returns)//6
    curve=temporal_smoothness_curve(log_returns=log_returns,
                                    window_length=window_length)
    

    abrupts = Abruptness_detector(curve)
    smooth = gaussian_filter1d(curve, sigma=2)

    idx = np.arange(len(curve))
    abs_a = np.abs(abrupts)

    normal = np.where(abs_a < 1)[0] + 1
    moderate = np.where((abs_a >= 1) & (abs_a < 2))[0] + 1
    catastrophic = np.where(abs_a >= 2)[0] + 1

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=idx, y=curve, name="Original", opacity=0.35))
    fig.add_trace(go.Scatter(x=idx, y=smooth, name="Smoothed"))

    fig.add_trace(go.Scatter(
        x=normal, y=curve[normal],
        mode="markers", name="Normal",
        marker=dict(color="green", size=6)
    ))

    fig.add_trace(go.Scatter(
        x=moderate, y=curve[moderate],
        mode="markers", name="Moderate",
        marker=dict(color="orange", size=9)
    ))

    fig.add_trace(go.Scatter(
        x=catastrophic, y=curve[catastrophic],
        mode="markers", name="Catastrophic",
        marker=dict(color="red", size=12)
    ))

    fig.update_layout(
        title="Temporal Smoothness with Abruptness Severity",
        xaxis_title="Time",
        yaxis_title="Smoothness",
        hovermode="x unified"
    )

    return fig