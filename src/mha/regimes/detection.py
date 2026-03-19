import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta
from sklearn.cluster import KMeans
from mha.returns.base import fetch_separation_time,realized_price_proxy_at,Calculate_log_returns_at_an_instance
from mha.data.fetch import get_my_data
from mha.evaluation.stability import temporal_smoothness_curve


def flag_monthly_regime(symbol: str,
                        window_length: int | None = None,
                        lookback: int|None = None) -> dict:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.
    if lookback is None:
        lookback=5
    

    month_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

 

    # Step 2-- Statistical feature construction

    # Regime identification is performed on statistical estimates, not raw prices.

    # Horizon-wise return estimates are constructed.
    # Horizon-wise volatility estimates are constructed.
    # These estimates represent the statistical behavior of the market at each time index.

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

    if window_length is None:
        window_length = len(log_returns_instances) // 5

    monthly_vol_curve = temporal_smoothness_curve(
        log_returns_instances,
    )
    monthly_return_curve = np.array([
    np.mean(log_returns_instances[i:i + window_length])
    for i in range(len(log_returns_instances) - window_length + 1)
    ])

    state_matrix = np.column_stack(
        [monthly_return_curve, monthly_vol_curve]
    )


    n_regimes = min(5, len(state_matrix))

    kmeans = KMeans(
        n_clusters=n_regimes,
        n_init=20,
        random_state=42
    )

    regime_labels = kmeans.fit_predict(state_matrix)

    regime_times = time_instances[window_length:]

    monthly_regime_flag = {
        str(regime_times[i]): int(regime_labels[i])
        for i in range(len(regime_labels))
    }

    return {
        "symbol": symbol,
        "horizon": "M",
        "lookback": lookback,
        "window_length": window_length,
        "n_regimes": n_regimes,
        "regime_by_time": monthly_regime_flag,
    }

def flag_weekly_regime(symbol: str,
                        window_length: int | None = None,
                        lookback: int|None = None) -> dict:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.
    if lookback is None:
        lookback=2
    

    week_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

 

    # Step 2-- Statistical feature construction

    # Regime identification is performed on statistical estimates, not raw prices.

    # Horizon-wise return estimates are constructed.
    # Horizon-wise volatility estimates are constructed.
    # These estimates represent the statistical behavior of the market at each time index.

    horizon = 5
    time_instances = fetch_separation_time(horizon=horizon, df=week_data_fetch)
    time_instances = sorted(time_instances)

    if len(time_instances) < 2:
        raise ValueError("Insufficient data to compute returns")

    price_instances = [None] * len(time_instances)
    log_returns_instances = [None] * (len(time_instances) - 1)

    for i in range(len(time_instances)):
        price_instances[i] = realized_price_proxy_at(
            time=time_instances[i],
            df=week_data_fetch
        )

    for i in range(len(time_instances) - 1):
        log_returns_instances[i] = Calculate_log_returns_at_an_instance(
            current_Price=price_instances[i+1],
            last_horizon_price=price_instances[i]
        )

    log_returns_instances = np.asarray(log_returns_instances, dtype=float)

    if len(log_returns_instances) < 10:
        raise ValueError("Not enough data for stability diagnostics")

    if window_length is None:
        window_length = len(log_returns_instances) // 5

    weekly_vol_curve = temporal_smoothness_curve(
        log_returns_instances,
    )
    weekly_return_curve = np.array([
    np.mean(log_returns_instances[i:i + window_length])
    for i in range(len(log_returns_instances) - window_length + 1)
    ])

    state_matrix = np.column_stack(
        [weekly_return_curve, weekly_vol_curve]
    )


    n_regimes = min(5, len(state_matrix))

    kmeans = KMeans(
        n_clusters=n_regimes,
        n_init=20,
        random_state=42
    )

    regime_labels = kmeans.fit_predict(state_matrix)

    regime_times = time_instances[window_length:]

    weekly_regime_flag = {
        str(regime_times[i]): int(regime_labels[i])
        for i in range(len(regime_labels))
    }

    return {
        "symbol": symbol,
        "horizon": "W",
        "lookback": lookback,
        "window_length": window_length,
        "n_regimes": n_regimes,
        "regime_by_time": weekly_regime_flag,
    }

def flag_daily_regime(symbol: str,
                        window_length: int | None = None,
                        lookback: int|None = None) -> dict:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.
    if lookback is None:
        lookback=70//365
    

    day_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

 

    # Step 2-- Statistical feature construction

    # Regime identification is performed on statistical estimates, not raw prices.

    # Horizon-wise return estimates are constructed.
    # Horizon-wise volatility estimates are constructed.
    # These estimates represent the statistical behavior of the market at each time index.

    horizon = 1
    time_instances = fetch_separation_time(horizon=horizon, df=day_data_fetch)
    time_instances = sorted(time_instances)

    if len(time_instances) < 2:
        raise ValueError("Insufficient data to compute returns")

    price_instances = [None] * len(time_instances)
    log_returns_instances = [None] * (len(time_instances) - 1)

    for i in range(len(time_instances)):
        price_instances[i] = realized_price_proxy_at(
            time=time_instances[i],
            df=day_data_fetch
        )

    for i in range(len(time_instances) - 1):
        log_returns_instances[i] = Calculate_log_returns_at_an_instance(
            current_Price=price_instances[i+1],
            last_horizon_price=price_instances[i]
        )

    log_returns_instances = np.asarray(log_returns_instances, dtype=float)

    if len(log_returns_instances) < 10:
        raise ValueError("Not enough data for stability diagnostics")

    if window_length is None:
        window_length = len(log_returns_instances) // 5

    daily_vol_curve = temporal_smoothness_curve(
        log_returns_instances,
    )
    daily_return_curve = np.array([
    np.mean(log_returns_instances[i:i + window_length])
    for i in range(len(log_returns_instances) - window_length + 1)
    ])

    state_matrix = np.column_stack(
        [daily_return_curve, daily_vol_curve]
    )


    n_regimes = min(5, len(state_matrix))

    kmeans = KMeans(
        n_clusters=n_regimes,
        n_init=20,
        random_state=42
    )

    regime_labels = kmeans.fit_predict(state_matrix)

    regime_times = time_instances[window_length:]

    daily_regime_flag = {
        str(regime_times[i]): int(regime_labels[i])
        for i in range(len(regime_labels))
    }

    return {
        "symbol": symbol,
        "horizon": "D",
        "lookback": lookback,
        "window_length": window_length,
        "n_regimes": n_regimes,
        "regime_by_time": daily_regime_flag,
    }

def flag_annually_regime(symbol: str,
                        window_length: int | None = None,
                        lookback: int|None = None) -> dict:
    #  Step 1-- Data Ingestion

    #    Data Based on horizon is loaded and cleaned
    #      - Incomplete current-day records are removed.
    #      - Data is sorted chronologically.
    if lookback is None:
        lookback=15
    

    year_data_fetch = get_my_data(days=365 * lookback, symbol=symbol)

 

    # Step 2-- Statistical feature construction

    # Regime identification is performed on statistical estimates, not raw prices.

    # Horizon-wise return estimates are constructed.
    # Horizon-wise volatility estimates are constructed.
    # These estimates represent the statistical behavior of the market at each time index.

    horizon = 235
    time_instances = fetch_separation_time(horizon=horizon, df=year_data_fetch)
    time_instances = sorted(time_instances)

    if len(time_instances) < 2:
        raise ValueError("Insufficient data to compute returns")

    price_instances = [None] * len(time_instances)
    log_returns_instances = [None] * (len(time_instances) - 1)

    for i in range(len(time_instances)):
        price_instances[i] = realized_price_proxy_at(
            time=time_instances[i],
            df=year_data_fetch
        )

    for i in range(len(time_instances) - 1):
        log_returns_instances[i] = Calculate_log_returns_at_an_instance(
            current_Price=price_instances[i+1],
            last_horizon_price=price_instances[i]
        )

    log_returns_instances = np.asarray(log_returns_instances, dtype=float)

    if len(log_returns_instances) < 10:
        raise ValueError("Not enough data for stability diagnostics")

    if window_length is None:
        window_length = len(log_returns_instances) // 5

    annually_vol_curve = temporal_smoothness_curve(
        log_returns_instances,
    )
    annually_return_curve = np.array([
    np.mean(log_returns_instances[i:i + window_length])
    for i in range(len(log_returns_instances) - window_length + 1)
    ])

    state_matrix = np.column_stack(
        [annually_return_curve, annually_vol_curve]
    )


    n_regimes = min(5, len(state_matrix))

    kmeans = KMeans(
        n_clusters=n_regimes,
        n_init=20,
        random_state=42
    )

    regime_labels = kmeans.fit_predict(state_matrix)

    regime_times = time_instances[window_length:]

    annually_regime_flag = {
        str(regime_times[i]): int(regime_labels[i])
        for i in range(len(regime_labels))
    }

    return {
        "symbol": symbol,
        "horizon": "Y",
        "lookback": lookback,
        "window_length": window_length,
        "n_regimes": n_regimes,
        "regime_by_time": annually_regime_flag,
    }