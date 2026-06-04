<h1 align="center">mha-finance</h1>

<p align="center">
  <b>Multi-Horizon Statistical Modeling for Financial Time Series</b>
</p>

<p align="center">
  A Python framework for descriptive statistical analysis of financial assets across multiple time horizons.
</p>

---

## Overview

**mha-finance** is a Python framework for **multi-horizon statistical modeling of financial time series**.

It is designed to help users **characterize**, not predict, the behavior of financial assets across different horizons such as **weekly, monthly, and annual windows**.

The library focuses on three core analytical tasks:

- **Return characterization**
- **Volatility characterization**
- **Market regime characterization**

Instead of forecasting prices or generating trading signals, `mha-finance` provides **descriptive and inferential statistical summaries** built from historical market data.

---
#### View Documentation at : https://vkverma9534.github.io/mha-finance/
---

## Installation

Install directly from PyPI:

```bash
pip install mha-finance
```

---

## Quick Start

`mha-finance` provides a **Trigger API** for quick first-time usage.

These are the easiest entry points into the library.

---

# 1) Return Characterization

Estimate horizon-wise return statistics for a symbol.

```python
from mha.Trigger.returns import returns_trigger

result = returns_trigger(symbol="GS", horizon="M", lookback=5)
print(result)
```

### Example Output

```python
{
    'symbol': 'GS',
    'horizon': 'Monthly',
    'mean_returns_pct': 1.6549,
    'median_returns_pct': 1.0414,
    'time_weighted_mean_returns_pct': 2.3761,
    'dispersion_pct': 0.6611
}
```

### What it gives you

- mean realized return
- median realized return
- time-weighted average return
- return dispersion

---

# 2) Volatility Characterization

Estimate recent conditional variability and uncertainty.

```python
from mha.Trigger.volatility import volatility_trigger

result = volatility_trigger(
    symbol="GS",
    horizon="M",
    lookback=5,
    decay_parameter=0.985
)

print(result)
```

### Example Output

```python
{
    'symbol': 'GS',
    'horizon': 'M',
    'volatility': {
        'raw': 0.08059,
        'percent': 8.0593
    },
    'time_weighted_volatility': {
        'raw': 0.08433,
        'percent': 8.4326
    },
    'volatility_uncertainty': {
        'raw': 0.0001727,
        'percent': 0.01727
    },
    'relative_volatility_change': {
        'percent': 0.3194,
        'flag': 'Smooth (Safe)'
    }
}
```

### What it gives you

- estimated volatility
- time-weighted volatility
- uncertainty in volatility estimate
- relative change / stability signal

---

# 3) Market Regime Characterization

Identify statistically similar return-volatility environments over time.

```python
from mha.Trigger.regime import regime_trigger

result = regime_trigger(symbol="GS", horizon="M", lookback=5)
print(result)
```

### Example Output

```python
{
    'symbol': 'GS',
    'horizon': 'M',
    'lookback': 5,
    'window_length': 11,
    'n_regimes': 5,
    'regime_by_time': {
        ...
    }
}
```

### What it gives you

- number of identified regimes
- regime labels through time
- horizon-wise regime segmentation

---

## Example: Plot Regime Timeline

```python
import pandas as pd
import matplotlib.pyplot as plt

from mha.Trigger.regime import regime_trigger

# Run trigger
result = regime_trigger(symbol="GS", horizon="M", lookback=5)

data = result if isinstance(result, dict) else result.__dict__

df = pd.DataFrame(list(data["regime_by_time"].items()), columns=["date", "regime"])
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

plt.figure(figsize=(14, 4))
plt.step(df["date"], df["regime"], where="post", linewidth=2)
plt.scatter(df["date"], df["regime"], s=40)

plt.title(f"{data['symbol']} Regime Timeline", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Regime")
plt.yticks(range(data["n_regimes"]))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

# 4) Ticker Search Utility (Will be released in next version):

`mha-finance` now includes a lightweight ticker discovery utility for resolving company or asset names into Yahoo Finance ticker symbols.

```python
from mha.data.explore import TickerSearch

results = TickerSearch("Goldman Sachs")

print(results)
```
### Example Output

```python
[
    {
        "name": "Goldman Sachs Group Inc.",
        "ticker": "GS"
    }
]
```
`TickerSearch` helps users discover valid ticker symbols by searching Yahoo Finance for matching companies or organizations. 
It is useful for quick asset lookup, exploratory analysis, and automated financial workflows.

---

## Design Philosophy

`mha-finance` is built around a simple idea:

> Financial behavior changes across time horizons, and each horizon should be studied statistically on its own terms.

This package is designed for:

- statistical exploration
- reproducible financial analysis
- academic / educational use
- horizon-aware market characterization

This package is **not** intended for:

- price prediction
- market timing
- trading signals
- portfolio optimization
- investment advice

---

## API Structure

`mha-finance` is organized into **two usage layers**:

### 1) Trigger API (Recommended for most users)

High-level entry points for fast analysis:

- `returns_trigger(...)`
- `volatility_trigger(...)`
- `regime_trigger(...)`

Use this layer when you want quick statistical summaries with minimal setup.

---

### 2) Base Analytical Functions

Under the trigger layer, the library contains several lower-level analytical functions that can be used independently for:

- custom workflows
- experimentation
- modular research pipelines
- advanced extension and development

This makes `mha-finance` suitable for both:

- **beginners who want quick outputs**
- **advanced users who want analytical control**

---

## Core Objectives

The framework is built around three statistical objectives:

### 1. Horizon-wise Return Characterization

Estimate and summarize realized returns over a selected horizon using historical price data.

Includes:

- horizon-based log returns
- rolling estimation windows
- mean / median return statistics
- dispersion and uncertainty analysis

---

### 2. Horizon-wise Volatility Characterization

Estimate recent conditional variability of returns without forecasting future volatility.

Includes:

- rolling variance / standard deviation
- EWMA-based estimation
- stability and uncertainty diagnostics
- horizon-aware volatility summaries

---

### 3. Horizon-wise Market Regime Characterization

Identify recurring statistical states of the market based on return-volatility structure.

Includes:

- statistical feature construction
- unsupervised regime partitioning
- regime labels across time
- descriptive market state summaries

---

## Data Source

`mha-finance` retrieves historical market data at runtime using **Yahoo Finance** through the [`yfinance`](https://pypi.org/project/yfinance/) Python library.

### Data Handling Policy

The framework follows a **non-redistributive** data usage model:

- No raw OHLCV or intraday datasets are bundled with the package
- No historical market datasets are shipped in the repository
- No price data is redistributed by this project
- Raw data is used only during runtime for statistical computation

---

## Important Disclaimer

`mha-finance` is an **analytical and educational framework**.

It is intended for:

- statistical analysis
- research workflows
- exploratory finance studies

It is **not** intended to provide:

- investment advice
- buy/sell recommendations
- trading signals
- guaranteed market insight

All outputs should be interpreted as **descriptive statistical summaries**, not predictive financial guidance.

---

## Why This Library Exists

Most financial tooling is built around one of two extremes:

- very basic charting and indicators
- fully predictive / trading-oriented pipelines

`mha-finance` is built for the space in between:

> **serious descriptive statistical analysis of financial time series across multiple horizons**

It aims to provide a cleaner foundation for users who want to study market behavior rigorously before jumping into forecasting or decision systems.

---

## Roadmap

Planned and possible future directions include:

- richer uncertainty summaries
- extended horizon support
- improved regime diagnostics
- enhanced visualization utilities
- more modular lower-level statistical tools

---


