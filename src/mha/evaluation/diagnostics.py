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