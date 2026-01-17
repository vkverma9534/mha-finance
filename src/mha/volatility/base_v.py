import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def volatility_estimation(
    log_returns_instances:np.ndarray)-> float:
    return np.sqrt(np.var(log_returns_instances))

def time_weighted_volatility(
    horizon:str,
    log_returns: np.ndarray,
    decay_parameter: float | None = None
) -> float:
    if decay_parameter == None:
        if(horizon=="Month"):
            decay_parameter=0.985
        if(horizon=="Year"):
            decay_parameter=0.995
        if(horizon=="Week"):
            decay_parameter=0.97
        if(horizon=="Day"):
            decay_parameter=0.94

    if not 0 < decay_parameter < 1:
        raise ValueError("decay_parameter must be between 0 and 1")

    if log_returns.ndim != 1 or len(log_returns) == 0:
        raise ValueError("log_returns must be a non-empty 1D array")

    n = len(log_returns)

    weights = (1 - decay_parameter) * decay_parameter ** np.arange(n - 1, -1, -1)
    weights /= weights.sum()

    variance = np.sum(weights * log_returns ** 2)
    return np.sqrt(variance)

