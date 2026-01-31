import numpy as np
import pytest

from mha.evaluation.stability import (
    volatility_uncertainty_dispersion,
    relative_volatility_change,
    temporal_smoothness_curve,
)


def test_volatility_uncertainty_dispersion_basic():
    x = np.random.randn(30)
    out = volatility_uncertainty_dispersion(x)
    assert isinstance(out, float)
    assert out >= 0.0

def test_volatility_uncertainty_dispersion_small_input():
    x = np.array([0.1, -0.2])
    out = volatility_uncertainty_dispersion(x)
    assert isinstance(out, float)

def test_volatility_uncertainty_dispersion_deterministic():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    out = volatility_uncertainty_dispersion(x, w_min=2)
    assert out >= 0.0



def test_relative_volatility_change_basic():
    x = np.array([0.2, -0.1, 0.3, -0.2])
    out = relative_volatility_change(x)
    assert isinstance(out, float)

def test_relative_volatility_change_short_input_raises():
    with pytest.raises(ValueError):
        relative_volatility_change(np.array([0.5]))

def test_relative_volatility_change_zero_volatility_raises():
    x = np.zeros(10)
    with pytest.raises(ZeroDivisionError):
        relative_volatility_change(x)


# ------------------------------------------------------------------
# temporal_smoothness_curve
# ------------------------------------------------------------------

def test_temporal_smoothness_curve_default_window():
    x = np.random.randn(50)
    curve = temporal_smoothness_curve(x)
    assert curve.ndim == 1
    assert curve.size > 0

def test_temporal_smoothness_curve_custom_window():
    x = np.random.randn(20)
    window = 5
    curve = temporal_smoothness_curve(x, window_length=window)
    assert curve.shape == (len(x) - window + 1,)

def test_temporal_smoothness_curve_window_too_small():
    x = np.random.randn(10)
    with pytest.raises(ValueError):
        temporal_smoothness_curve(x, window_length=1)

def test_temporal_smoothness_curve_deterministic():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    curve = temporal_smoothness_curve(x, window_length=2)

    expected = np.array([
        np.std([1.0, 2.0], ddof=1),
        np.std([2.0, 3.0], ddof=1),
        np.std([3.0, 4.0], ddof=1),
    ])

    np.testing.assert_allclose(curve, expected)
