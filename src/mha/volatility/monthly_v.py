import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta


def find_monthly_stability(symbol: str,
                           decay_parameter: float | None = None, 
                           lookback: float | None = None, 
                           window_length: int | None = None) -> dict:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.
    if lookback is None:
        lookback=5

    if decay_parameter is not None and not (0 < decay_parameter < 1):
        raise ValueError("decay_parameter must be in (0, 1)")

    month_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

 

    # Step 2-- Return Construction

    #    Horizon-based log returns are computed from closing prices for each
    #    interval specified by the horizon selection (see 3):
    #      - Let P_t be the closing price on day t.
    #      - Declare horizon (H) based on selection of user
    #              (eg. H=21 for Monthly horizon by user)
    #      - The return ending at at time t is:
    #                       r_t^(H) = log(P_t) - log(P_{t-H})
    #      This produces a time series of realized monthly returns.

    horizon = 22
    time_instances = fetch_separation_time(horizon=horizon, df=month_data_fetch)
    time_instances = sorted(time_instances)

    if len(time_instances) < 2:
        raise ValueError("Insufficient data to compute returns")

    price_instances = [None] * len(time_instances)
    log_returns_instances = [None] * (len(time_instances) - 1)

    for i in range(len(time_instances)):
        price_instances[i] = realized_price_proxy_at(
            time=time_instances[i],
            df=month_data_fetch
        )

    for i in range(len(time_instances) - 1):
        log_returns_instances[i] = Calculate_log_returns_at_an_instance(
            current_Price=price_instances[i+1],
            last_horizon_price=price_instances[i]
        )

    log_returns_instances = np.asarray(log_returns_instances, dtype=float)

    if len(log_returns_instances) < 10:
        raise ValueError("Not enough data for stability diagnostics")
    
    # Step 4-- Statistical volatility estimation

    # Within each rolling window,, volatility is estimated using statistical estimators, not predictive models

    # Typical estimators include:

    # Sample varince σ^2 = (1(W-1))*∑(rt-rˉ)^2
    # Rolling standard deviation σ = (σ^2)^(1/2)
    # Exponentially Weighted Moving Average (EWMA) σ(t)^2 = λσ(t-1)^2 + (1-λ)r(t)^2
    # These estimators characterize recent conditional variability. not future risk.
    deliverables = {
    "volatility": volatility_estimation(log_returns_instances),
    "time_weighted_volatility": time_weighted_volatility(
        horizon="Month",
        log_returns=log_returns_instances,
        decay_parameter=decay_parameter
    ),
    "volatility_dispersion": volatility_uncertainty_dispersion(
        log_returns=log_returns_instances
    ),
    "relative_volatility_change": relative_volatility_change(
        log_returns=log_returns_instances
    ),
    "temporal_smoothness_curve": temporal_smoothness_curve(
        log_returns_instances,
        window_length=window_length
    ),
    }

    return deliverables
