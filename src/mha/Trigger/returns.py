import numpy as np
import math
from typing import List
import pandas as pd
from datetime import datetime, timezone, timedelta

def returns_trigger(symbol: str,
                    horizon: str,
                    lookback:float|None=None,
                    decay_parameter:float|None=None):
    if(horizon=="M"):
        deliverables=find_monthly_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if(horizon=="A"):
        deliverables=find_annaul_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if(horizon=="W"):
        deliverables=find_weekly_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
    if(horizon=="D"):
        deliverables=find_daily_estimations(symbol=symbol,
                                              lookback=lookback,
                                              decay_parameter=decay_parameter)
        

    print(f"symbol: {symbol}")
    if(horizon=="M"):
        print(f"Horizon: Monthly")
    if(horizon=="A"):
        print(f"Horizon: Annual")
    if(horizon=="W"):
        print(f"Horizon: Weekly")
    if(horizon=="D"):
        print(f"Horizon: Daily")
    print(f"Mean Returns: {deliverables[0]*100}%")
    print(f"Median Returns: {deliverables[1]*100}%")
    print(f"Time Weighted Mean Returns: {deliverables[2]*100}%")
    print(f"Dispersion: {deliverables[3]*100}%")