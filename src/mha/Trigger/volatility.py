import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def volatility_trigger(symbol: str,
                    horizon: str,
                    lookback:float|None=None,
                    decay_parameter:float|None=None,
                    window_length:float|None=None):
    if(horizon=="M"):
        deliverables=find_monthly_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    if(horizon=="A"):
        deliverables=find_annaully_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    if(horizon=="W"):
        deliverables=find_weekly_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
    if(horizon=="D"):
        deliverables=find_daily_stability(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter,
                                              window_length=window_length)
        

    print(f"symbol: {symbol}")
    if(horizon=="M"):
        print(f"Horizon: Monthly")
    if(horizon=="A"):
        print(f"Horizon: Annual")
    if(horizon=="W"):
        print(f"Horizon: Weekly")
    if(horizon=="D"):
        print(f"Horizon: Daily")
    print(f"Volatility of Returns: {deliverables["volatility"]*100}%")
    print(f"Time Weighted Volatilty of Returns: {deliverables["time_weighted_volatility"]*100}%")
    print(f"Volatility Uncertainty: {deliverables["volatility_dispersion"]*100}%")
    cond_num = deliverables["relative_volatility_change"] * 100

    if abs(cond_num) < 2:
        flag = "Smooth (Safe)"
    elif abs(cond_num) < 8:
        flag = "Moderate"
    else:
        flag = "High (Unsafe)"

    print(f"Relative Volatility Change (Condition Number): {cond_num:.2f}% → {flag}")