#annually.py

import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta


def annual_time_weighted_returns(
    log_returns: np.ndarray,
    decay_parameter: float | None = None
) -> float:
    if decay_parameter is None:
        decay_parameter = 0.88  # healthy default for yearly data
    if not (0 < decay_parameter < 1):
        raise ValueError("decay_parameter must be in (0, 1)")
    r = log_returns[::-1]
    n = len(r)
    weights = (1 - decay_parameter) * decay_parameter ** np.arange(n)
    weights /= weights.sum()

    return float(np.dot(weights, r))

def find_annaul_estimations(symbol: str, decay_parameter: float, lookback: float | None = None) -> np.ndarray:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.

    if lookback is None:
        lookback=15

    annual_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

    # Step 2-- Return Construction

    #    Horizon-based log returns are computed from closing prices for each
    #    interval specified by the horizon selection (see 3):
    #      - Let P_t be the closing price on day t.
    #      - Declare horizon (H) based on selection of user
    #              (eg. H=21 for Monthly horizon by user)
    #      - The return ending at at time t is:
    #                       r_t^(H) = log(P_t) - log(P_{t-H})
    #      This produces a time series of realized monthly returns.

    horizon = 233
    time_instances = fetch_separation_time(horizon=horizon, df=annual_data_fetch)
    time_instances = sorted(time_instances)

    price_instances = [None] * len(time_instances)
    log_returns_instances = [None] * (len(time_instances) - 1)

    for i in range(len(time_instances)):
        price_instances[i] = realized_price_proxy_at(
            time=time_instances[i],
            df=annual_data_fetch
        )

    for i in range(len(time_instances) - 1):
        log_returns_instances[i] = Calculate_log_returns_at_an_instance(
            current_Price=price_instances[i],
            last_horizon_price=price_instances[i + 1]
        )

    log_returns_instances = np.asarray(log_returns_instances, dtype=float)

    #  Step 4-- Statistical estimation

    #     Within Rolling Window
    #    - Mean horizon return (μ̂^(H))
    #        μ̂^(H) = (1 / W) * Σ r_t^(H)
    #        Represents the average realized Horizon return.
    #    - Return dispersion (sample Variance)
    #         D̂^(H) = (1 / (W − 1)) * Σ (r_t^(H) − μ̂^(H))²
    #     Represents the empirical dispersion of monthly returns
    #          (not volatility modeling)

    deliverables = np.array([
        calculating_mean_horizon_return(log_returns=log_returns_instances),
        median_return(log_returns=log_returns_instances),
        annual_time_weighted_returns(
            log_returns=log_returns_instances,
            decay_parameter=decay_parameter
        ),
        dispersion(log_returns=log_returns_instances)
    ], dtype=float)

    return deliverables