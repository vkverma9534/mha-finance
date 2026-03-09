import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

def fetch_daily_ohlcv(    #-> For estimating all scenarios other than intraday
    symbol: str,
    start: str,
    end: str | None = None,
    interval: str = "1d"
) -> pd.DataFrame:
    if end is None:
        end = datetime.now(timezone.utc)

    df = yf.download(
        tickers=symbol,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        raise ValueError("No data fetched — check interval/date limits")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    df = df.rename(columns={
    "Date": "timestamp",
    "Datetime": "timestamp",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    now = pd.Timestamp.utcnow().floor("1d")
    df = df[df["timestamp"] < now]

    return df[["timestamp", "open", "high", "low", "close", "volume"]]

def get_my_data(
    days: int,
    symbol: str
) -> pd.DataFrame:
    data_start = datetime.now(timezone.utc) - timedelta(days=days)

    data_fetch = fetch_daily_ohlcv(
        symbol=symbol,
        start=data_start,
        interval="1d",
        end=datetime.now(timezone.utc) - timedelta(days=1)
    )

    if isinstance(data_fetch.index, pd.DatetimeIndex):
        data_fetch = data_fetch.sort_index()
    else:
        time_col = next(
            col for col in data_fetch.columns
            if col.lower() in {"timestamp", "date", "datetime", "time"}
        )

        data_fetch[time_col] = pd.to_datetime(
            data_fetch[time_col],
            utc=True,
            errors="coerce"
        )

    data_fetch = (
        data_fetch
        .dropna(subset=[time_col])
        .sort_values(time_col)
        .set_index(time_col)
    )

    ohlc_cols = ["open", "high", "low", "close"]
    data_fetch[ohlc_cols] = data_fetch[ohlc_cols].apply(
        pd.to_numeric,
        errors="coerce"
    )

    data_fetch = data_fetch.dropna(subset=ohlc_cols)
    data_fetch = data_fetch[(data_fetch[ohlc_cols] > 0).all(axis=1)]
    return data_fetch

