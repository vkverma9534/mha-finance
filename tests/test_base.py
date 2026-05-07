import math
import numpy as np
import pandas as pd
import pytest
from datetime import datetime

from mha.returns.base import (
    realized_price_proxy_at,
    fetch_separation_time,
    Calculate_log_returns_at_an_instance,
    calculating_mean_horizon_return,
    median_return,
    dispersion,
)

def test_realized_price_proxy_at_valid():
    idx = pd.to_datetime(["2024-01-01"])
    df = pd.DataFrame(
        {
            "open": [100],
            "high": [110],
            "low": [90],
            "close": [105],
        },
        index=idx,
    )

    result = realized_price_proxy_at(idx[0], df)
    assert result == pytest.approx((100 + 110 + 90 + 105) / 4)


def test_realized_price_proxy_at_missing_timestamp():
    df = pd.DataFrame(
        {
            "open": [100],
            "high": [110],
            "low": [90],
            "close": [105],
        },
        index=pd.to_datetime(["2024-01-01"]),
    )

    with pytest.raises(ValueError, match="No data found"):
        realized_price_proxy_at(pd.Timestamp("2024-01-02"), df)


def test_realized_price_proxy_at_non_finite_values():
    idx = pd.to_datetime(["2024-01-01"])
    df = pd.DataFrame(
        {
            "open": [np.nan],
            "high": [110],
            "low": [90],
            "close": [105],
        },
        index=idx,
    )

    with pytest.raises(ValueError, match="Invalid OHLC values"):
        realized_price_proxy_at(idx[0], df)


def test_realized_price_proxy_at_non_positive_values():
    idx = pd.to_datetime(["2024-01-01"])
    df = pd.DataFrame(
        {
            "open": [100],
            "high": [110],
            "low": [0],
            "close": [105],
        },
        index=idx,
    )

    with pytest.raises(ValueError, match="Non-positive OHLC values"):
        realized_price_proxy_at(idx[0], df)

def test_fetch_separation_time_basic():
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    df = pd.DataFrame(index=idx)

    result = fetch_separation_time(horizon=2, df=df)

    expected = np.array([
        pd.Timestamp("2024-01-05"),
        pd.Timestamp("2024-01-03"),
        pd.Timestamp("2024-01-01"),
    ])

    assert np.array_equal(result, expected)


def test_fetch_separation_time_horizon_one():
    idx = pd.date_range("2024-01-01", periods=3, freq="D")
    df = pd.DataFrame(index=idx)

    result = fetch_separation_time(horizon=1, df=df)

    expected = np.array([
        pd.Timestamp("2024-01-03"),
        pd.Timestamp("2024-01-02"),
        pd.Timestamp("2024-01-01"),
    ])

    assert np.array_equal(result, expected)

def test_calculate_log_returns():
    current = 110
    past = 100

    result = Calculate_log_returns_at_an_instance(current, past)

    assert result == pytest.approx(math.log(1.1))


def test_calculate_log_returns_equal_prices():
    result = Calculate_log_returns_at_an_instance(100, 100)
    assert result == 0.0

def test_calculating_mean_horizon_return():
    data = np.array([0.01, 0.02, 0.03])
    assert calculating_mean_horizon_return(data) == pytest.approx(0.02)


def test_median_return():
    data = np.array([0.01, 0.03, 0.02])
    assert median_return(data) == pytest.approx(0.02)


def test_dispersion_sample_variance():
    data = np.array([1.0, 2.0, 3.0])
    # sample variance with ddof=1 → 1.0
    assert dispersion(data) == pytest.approx(1.0)


def test_calculate_log_returns_non_positive_prices():
    with pytest.raises(ValueError, match="Prices must be positive"):
        Calculate_log_returns_at_an_instance(100, 0)

    with pytest.raises(ValueError, match="Prices must be positive"):
        Calculate_log_returns_at_an_instance(-100, 50)
