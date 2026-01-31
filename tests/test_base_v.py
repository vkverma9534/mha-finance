import numpy as np
import pytest

from mha.volatility.base_v import (
    volatility_estimation,
    time_weighted_volatility,
)


def test_volatility_estimation_basic():
    x = np.array([1.0, 2.0, 3.0])
    out = volatility_estimation(x)
    assert isinstance(out, float)

def test_volatility_estimation_zero():
    x = np.zeros(10)
    out = volatility_estimation(x)
    assert out == 0.0

def test_volatility_estimation_deterministic():
    x = np.array([1.0, 3.0])
    expected = np.sqrt(np.var(x))
    out = volatility_estimation(x)
    assert out == expected



@pytest.mark.parametrize(
    "horizon",
    ["Day", "Week", "Month", "Year"],
)
def test_time_weighted_volatility_default_horizon(horizon):
    x = np.random.randn(20)
    out = time_weighted_volatility(horizon, x)
    assert isinstance(out, float)
    assert out >= 0.0

def test_time_weighted_volatility_custom_decay():
    x = np.array([0.1, -0.2, 0.3])
    out = time_weighted_volatility("Day", x, decay_parameter=0.9)
    assert isinstance(out, float)

def test_time_weighted_volatility_invalid_decay_raises():
    x = np.random.randn(10)
    with pytest.raises(ValueError):
        time_weighted_volatility("Day", x, decay_parameter=1.5)

def test_time_weighted_volatility_empty_input_raises():
    with pytest.raises(ValueError):
        time_weighted_volatility("Day", np.array([]))

def test_time_weighted_volatility_non_1d_input_raises():
    with pytest.raises(ValueError):
        time_weighted_volatility("Day", np.array([[1.0, 2.0]]))

def test_time_weighted_volatility_deterministic():
    x = np.array([1.0, 2.0, 3.0])
    decay = 0.5

    weights = (1 - decay) * decay ** np.arange(len(x) - 1, -1, -1)
    weights /= weights.sum()
    expected = np.sqrt(np.sum(weights * x ** 2))

    out = time_weighted_volatility("Day", x, decay_parameter=decay)
    np.testing.assert_allclose(out, expected)
