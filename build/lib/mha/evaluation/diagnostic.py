from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter1d
from typing import Optional
from mha.evaluation.stability import temporal_smoothness_curve



def Abruptness_detector(temporal_smoothness_curve: np.ndarray) -> np.ndarray:
    if len(temporal_smoothness_curve) < 2:
        return np.array([], dtype=float)

    std = np.std(temporal_smoothness_curve)
    if std == 0:
        return np.zeros(len(temporal_smoothness_curve) - 1, dtype=float)

    return np.diff(temporal_smoothness_curve) / std


def diagnostics(log_returns: np.ndarray, window_length: int | None = None) -> go.Figure:
    if window_length is None:
        window_length = len(log_returns) // 6

    curve = temporal_smoothness_curve(log_returns, window_length)
    abrupts = Abruptness_detector(curve)
    smooth = gaussian_filter1d(curve, sigma=2)

    idx = np.arange(len(curve))
    abs_a = np.abs(abrupts)

    normal = np.where(abs_a < 1)[0] + 1
    moderate = np.where((abs_a >= 1) & (abs_a < 2))[0] + 1
    catastrophic = np.where(abs_a >= 2)[0] + 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=idx, y=curve, name="Original", opacity=0.35))
    fig.add_trace(go.Scatter(x=idx, y=smooth, name="Smoothed"))
    fig.add_trace(go.Scatter(x=normal, y=curve[normal], mode="markers", name="Normal"))
    fig.add_trace(go.Scatter(x=moderate, y=curve[moderate], mode="markers", name="Moderate"))
    fig.add_trace(go.Scatter(x=catastrophic, y=curve[catastrophic], mode="markers", name="Catastrophic"))
    return fig

class AbruptnessDetector:
    def __init__(self, threshold_normal: float = 1.0, threshold_moderate: float = 2.0):
        self.threshold_normal = threshold_normal
        self.threshold_moderate = threshold_moderate

    def compute(self, curve: np.ndarray) -> np.ndarray:
        return Abruptness_detector(curve)

    def classify(self, abruptness: np.ndarray) -> dict[str, np.ndarray]:
        a = np.abs(abruptness)
        return {
            "normal": np.where(a < self.threshold_normal)[0] + 1,
            "moderate": np.where(
                (a >= self.threshold_normal) & (a < self.threshold_moderate)
            )[0] + 1,
            "catastrophic": np.where(a >= self.threshold_moderate)[0] + 1,
        }
    
    def compute(self, curve: np.ndarray) -> np.ndarray:
        if curve.ndim != 1:
            raise ValueError("curve must be 1D")
        return Abruptness_detector(curve)


class TemporalDiagnostics:
    def __init__(self, detector: Optional[AbruptnessDetector] = None, smoothing_sigma: float = 2.0):
        self.detector = detector or AbruptnessDetector()
        self.smoothing_sigma = smoothing_sigma

    def compute_curve(self, log_returns: np.ndarray, window_length: int) -> np.ndarray:
        raise NotImplementedError

    def run(self, log_returns: np.ndarray, window_length: int | None = None) -> go.Figure:
        if log_returns.ndim != 1:
            raise ValueError("log_returns must be 1D")

        if window_length is None:
            window_length = len(log_returns) // 6

        curve = self.compute_curve(log_returns, window_length)
        abrupt = self.detector.compute(curve)
        smooth = gaussian_filter1d(curve, sigma=self.smoothing_sigma)
        regimes = self.detector.classify(abrupt)

        idx = np.arange(len(curve))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=idx, y=curve, name="Original", opacity=0.35))
        fig.add_trace(go.Scatter(x=idx, y=smooth, name="Smoothed"))
        fig.add_trace(go.Scatter(x=regimes["normal"], y=curve[regimes["normal"]], mode="markers", name="Normal"))
        fig.add_trace(go.Scatter(x=regimes["moderate"], y=curve[regimes["moderate"]], mode="markers", name="Moderate"))
        fig.add_trace(go.Scatter(x=regimes["catastrophic"], y=curve[regimes["catastrophic"]], mode="markers", name="Catastrophic"))
        return fig
