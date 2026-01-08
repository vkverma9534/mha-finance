import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def realized_price_proxy_at(
    time: pd.Timestamp,
    df: pd.DataFrame
) -> float:
    try:
        prices = df.loc[time, ["open", "high", "low", "close"]].values
    except KeyError:
        raise ValueError(f"No data found for timestamp {time}")

    if not np.isfinite(prices).all():
        raise ValueError(f"Invalid OHLC values at {time}")

    if (prices <= 0).any():
        raise ValueError(f"Non-positive OHLC values at {time}")

    return float(prices.mean())

def fetch_separation_time(
    horizon: int,
    df: pd.DataFrame,
) -> np.ndarray:

    time_instances: List[datetime] = []

    total_rows = len(df)
    i = 0

    while total_rows - i - 1 >= 0:
        time_instance = df.index[total_rows - i - 1]
        time_instance=pd.to_datetime(time_instance)
        time_instances.append(time_instance)
        i += horizon

    return np.array(time_instances)

def Calculate_log_returns_at_an_instance(
    current_Price: float,
    last_horizon_price:float,
) -> float:
    return math.log(current_Price / last_horizon_price)

#  Step 3-- Statistical estimation

#     Within Rolling Window
#    - Mean horizon return (μ̂^(H))
#        μ̂^(H) = (1 / W) * Σ r_t^(H)
#        Represents the average realized Horizon return.
#    - Return dispersion (sample Variance)
#         D̂^(H) = (1 / (W − 1)) * Σ (r_t^(H) − μ̂^(H))²
#     Represents the empirical dispersion of monthly returns
#          (not volatility modeling)

def calculating_mean_horizon_return(log_returns: np.ndarray) -> float:
    return log_returns.mean()

def median_return(log_returns: np.ndarray) -> float:
    return np.median(log_returns)

def dispersion(log_returns: np.ndarray) -> float:
    return np.var(log_returns, ddof=1)