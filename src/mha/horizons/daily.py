#Daily.py

import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

#  Step 1-- Data Ingestion

#    Data Based on horizon is loaded and cleaned
#      - Incomplete current-day records are removed.
#      - Data is sorted chronologically.

week_data_start = datetime.now(timezone.utc) - timedelta(days=60)

week_data_fetch = fetch_daily_ohlcv(
    symbol="AAPL",
    start=year_data_start,
    interval="1d",
    end = datetime.now(timezone.utc)-timedelta(days=1)
)

week_data_fetch=week_data_fetch.sort_values(by="timestamp")


# Step 2-- Return Construction

#    Horizon-based log returns are computed from closing prices for each
#    interval specified by the horizon selection (see 3):
#      - Let P_t be the closing price on day t.
#      - Declare horizon (H) based on selection of user
#              (eg. H=21 for Monthly horizon by user)
#      - The return ending at at time t is:
#                       r_t^(H) = log(P_t) - log(P_{t-H})
#      This produces a time series of realized monthly returns.


# assuming price as average of "OHLC" features
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
# Use case for Price_at_instance_t()
# P = Price_at_instance_t(
#     time="2020-12-28 00:00:00+00:00",
#     df=year_data_fetch
# )

Horizon=1  # number of working days in a week for stock exchange



def fetch_separation_time(
    horizon: int,
    df: pd.DataFrame,
) -> np.ndarray:

    time_instances: List[datetime] = []

    total_rows = len(df)
    i = 0

    while total_rows - i - 1 >= 0:
        time_instance = df.iloc[total_rows - i - 1]["timestamp"]
        time_instances.append(time_instance)
        i += horizon

    return np.array(time_instances)

#Use Case
# time = fetch_separation_time(
#       horizon=5,
#       df=year_data_fetch,
#   )
# time.size

def Calculate_log_returns_at_an_instance(
    current_Price: float,
    last_horizon_price,
) -> float:
    return math.log(current_Price / last_horizon_price)

#  Step 3-- Rolling estimation window

#   Rolling estimation window
#    - W = Data Span for the horizon / Horizon Length.
#    - Returns inside the window are assumed locally stationary.
#    - This Window defines the data used for estimation.
#    - Each rolling window defines the data used for statistical estimation.

Window = len(year_data_fetch)/Horizon

#  Step 4-- Statistical estimation

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


def time_weighted_returns(
    log_returns: np.ndarray,
    decay_parameter: float | None = None
) -> float:
    if decay_parameter is None:
        decay_parameter = 0.94  # healthy default for monthly data
    if not (0 < decay_parameter < 1):
        raise ValueError("decay_parameter must be in (0, 1)")
    r = log_returns[::-1]
    n = len(r)
    weights = (1 - decay_parameter) * decay_parameter ** np.arange(n)
    weights /= weights.sum()
    return float(np.dot(weights, r))


def dispersion(returns: np.ndarray) -> float:
    return np.var(returns, ddof=1)