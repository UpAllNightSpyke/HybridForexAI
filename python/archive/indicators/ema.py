import MetaTrader5 as mt5
import pandas as pd
from .indicator_library import AppliedPrice, Method

# Define the parameters for the EMA indicator
indicator_params = ['period', 'shift', 'method', 'applied_price']

def calculate_ema(data, symbol, timeframe, params):
    print("Calculating EMA using MT5...")
    period = int(params.get('period', 14))
    shift = int(params.get('shift', 0))
    method = Method[params.get('method', 'EMA')].value
    applied_price = AppliedPrice[params.get('applied_price', 'CLOSE')].value

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get EMA values using MT5 built-in function
    ema_values = mt5.iMA(symbol, timeframe, period, shift, method, applied_price, len(rates))
    if ema_values is None:
        print(f"Error: No EMA data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['EMA'] = ema_values[-len(data):]  # Align with the length of the data
    
    # Set NaN EMA values to 0
    data['EMA'].fillna(0, inplace=True)
    
    return data