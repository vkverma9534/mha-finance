import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def Abruptness_detector(temporal_smoothness_curve: np.ndarray) -> np.ndarray:
    if len(temporal_smoothness_curve) < 2:
        return np.array([], dtype=float)

    std_dev_of_volatility = np.std(temporal_smoothness_curve)
    if std_dev_of_volatility == 0:
        return np.zeros(len(temporal_smoothness_curve) - 1, dtype=float)

    abruptness_index = []
    for i in range(len(temporal_smoothness_curve) - 1):
        abruptness_index.append(
            (temporal_smoothness_curve[i+1] - temporal_smoothness_curve[i])
            / std_dev_of_volatility
        )
    return np.asarray(abruptness_index, dtype=float)

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