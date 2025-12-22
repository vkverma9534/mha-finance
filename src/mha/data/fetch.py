import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta









def fetch_2minute_ohlcv(      #-> For estimating 1 week scenarios
    symbol: str,
    start: str,
    end: str | None = None,
    interval: str = "2m"
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
        "Datetime": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    now = pd.Timestamp.utcnow().floor("min")
    df = df[df["timestamp"] < now]

    return df[["timestamp", "open", "high", "low", "close", "volume"]]

# Use case

# intraday_start = datetime.now(timezone.utc) - timedelta(days=50)

# intraday_data_fetch = fetch_2minute_ohlcv(
#     symbol="AAPL",
#     start=intraday_start,
#     interval="2m"
# )



def fetch_daily_ohlcv(    #-> For estimating 1 year scenarios
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
#use case

# year_data_start = datetime.now(timezone.utc) - timedelta(days=365*10)

# year_data_fetch = fetch_daily_ohlcv(
#     symbol="AAPL",
#     start=year_data_start,
#     interval="1d"
# )
#--------------------------------------------------------------------
# use case

# week_data_start = datetime.now(timezone.utc) - timedelta(days=365*15)

# week_data_fetch = fetch_minute_ohlcv(
#     symbol="AAPL",
#     start=week_data_start,
#     interval="1d"
# )

#---------------------------------------------------------------------
#use case

# month_data_start = datetime.now(timezone.utc) - timedelta(days=365*5)

# month_data_fetch = fetch_hourly_ohlcv(
#     symbol="AAPL",
#     start=month_data_start,
#     interval="1d"
# )