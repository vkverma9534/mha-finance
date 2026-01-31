import numpy as np
import plotly.graph_objects as go
import pytest

from mha.evaluation.diagnostic import AbruptnessDetector,TemporalDiagnostics


class TestAbruptnessDetector:
    def test_empty_input(self):
        d=AbruptnessDetector()
        out=d.compute(np.array([]))
        assert out.size==0

    def test_single_element(self):
        d=AbruptnessDetector()
        out=d.compute(np.array([1.0]))
        assert out.size==0

    def test_zero_std(self):
        d=AbruptnessDetector()
        x=np.array([2.0,2.0,2.0])
        out=d.compute(x)
        assert np.all(out==0)

    def test_correct_values(self):
        d=AbruptnessDetector()
        x=np.array([1.0,2.0,4.0])
        std=np.std(x)
        expected=np.array([(2-1)/std,(4-2)/std])
        np.testing.assert_allclose(d.compute(x),expected)

    def test_non_1d_input_raises(self):
        d=AbruptnessDetector()
        with pytest.raises(ValueError):
            d.compute(np.array([[1.0,2.0]]))

    def test_classify_indices(self):
        d=AbruptnessDetector()
        abrupt=np.array([0.5,1.5,2.5])
        out=d.classify(abrupt)
        assert np.array_equal(out["normal"],np.array([1]))
        assert np.array_equal(out["moderate"],np.array([2]))
        assert np.array_equal(out["catastrophic"],np.array([3]))


class DummyDiagnostics(TemporalDiagnostics):
    def compute_curve(self,log_returns,window_length):
        return np.array([1.0,2.0,3.0,4.0])


class TestTemporalDiagnostics:
    def test_returns_figure(self):
        diag=DummyDiagnostics()
        fig=diag.run(np.random.randn(60))
        assert isinstance(fig,go.Figure)

    def test_trace_count(self):
        diag=DummyDiagnostics()
        fig=diag.run(np.random.randn(60))
        assert len(fig.data)==5

    def test_default_window_length(self):
        captured={}
        class CaptureDiagnostics(TemporalDiagnostics):
            def compute_curve(self,log_returns,window_length):
                captured["window_length"]=window_length
                return np.array([1.0,2.0,3.0])
        diag=CaptureDiagnostics()
        data=np.random.randn(60)
        diag.run(data)
        assert captured["window_length"]==len(data)//6

    def test_non_1d_log_returns_raises(self):
        diag=DummyDiagnostics()
        with pytest.raises(ValueError):
            diag.run(np.array([[1.0,2.0]]))

