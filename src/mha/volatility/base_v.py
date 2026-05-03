import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def volatility_estimation(log_returns_instances: np.ndarray) -> float:
    return float(np.std(log_returns_instances, ddof=1))

def time_weighted_volatility(
    horizon: str,
    log_returns: np.ndarray,
    decay_parameter: float | None = None
) -> float:

    if decay_parameter is None:
        if horizon[0].lower() == "m":
            decay = 0.985
        elif horizon[0].lower() == "a" or horizon[0].lower() == "y":
            decay = 0.995
        elif horizon[0].lower() == "w":
            decay = 0.97
        elif horizon[0].lower() == "d":
            decay = 0.94
        else:
            raise ValueError("Invalid horizon")
    else:
        decay = decay_parameter

    if not 0 < decay < 1:
        raise ValueError("decay_parameter must be between 0 and 1")

    if log_returns.ndim != 1 or len(log_returns) == 0:
        raise ValueError("log_returns must be a non-empty 1D array")

    n = len(log_returns)

    weights = (1 - decay) * decay ** np.arange(n - 1, -1, -1)
    weights /= weights.sum()

    variance = np.sum(weights * log_returns ** 2)

    return float(np.sqrt(variance))

