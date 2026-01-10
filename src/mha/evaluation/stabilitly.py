import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def volatility_uncertainty_dispersion(log_returns: np.ndarray, w_min: int = 2) -> float:
    n = len(log_returns)
    std_dev = []

    for w in range(w_min, n + 1):
        std_dev.append(volatility_estimation(log_returns[-w:]))

    std_dev = np.asarray(std_dev, dtype=float)
    return np.var(std_dev, ddof=1)

def condition_number(log_returns:np.ndarray)-> float:
    return volatility_estimation(log_returns)-volatility_estimation(log_returns[:-1])