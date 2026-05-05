import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta
from mha.volatility.base_v import volatility_estimation

def volatility_uncertainty_dispersion(log_returns: np.ndarray, w_min: int = 2) -> float:
    n = log_returns.size
    if n < w_min:
        raise ValueError("log_returns length must be >= w_min")

    vols = np.empty(n - w_min + 1)

    for i, w in enumerate(range(w_min, n + 1)):
        vols[i] = volatility_estimation(log_returns[-w:])

    return float(np.var(vols, ddof=1))

def relative_volatility_change(log_returns: np.ndarray) -> float:
    n = log_returns.size
    if n < 2:
        raise ValueError("log_returns must contain at least two elements")

    vol_full = float(volatility_estimation(log_returns))
    if vol_full == 0.0:
        raise ZeroDivisionError("Volatility estimation returned zero")

    vol_truncated = float(volatility_estimation(log_returns[:-1]))

    return (vol_full - vol_truncated) / vol_full

def temporal_smoothness_curve(
    log_returns: np.ndarray,
    window_length: int | None = None
) -> np.ndarray:
    if window_length is None:
        window_length = len(log_returns) // 5
    if window_length < 2:
        raise ValueError("window_length must be >= 2")

    volatility_curve = []

    for i in range(len(log_returns) - window_length + 1):
        window = log_returns[i:i + window_length]
        vol = np.std(window, ddof=1)
        volatility_curve.append(vol)

    return np.asarray(volatility_curve, dtype=float)
