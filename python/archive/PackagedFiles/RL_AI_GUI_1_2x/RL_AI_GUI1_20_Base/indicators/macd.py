import MetaTrader5 as mt5
import pandas as pd
from .indicator_library import AppliedPrice, Method

# Define the parameters for the MACD indicator
indicator_params = ['fast_ema_period', 'slow_ema_period', 'signal_period', 'applied_price']

def calculate_macd(data, symbol, timeframe, params):
    print("Calculating MACD using MT5...")
    fast_ema_period = int(params.get('fast_ema_period', 12))
    slow_ema_period = int(params.get('slow_ema_period', 26))
    signal_period = int(params.get('signal_period', 9))
    applied_price = AppliedPrice[params.get('applied_price', 'CLOSE')].value

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + slow_ema_period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get MACD values using MT5 built-in function
    macd_values = mt5.iMACD(symbol, timeframe, fast_ema_period, slow_ema_period, signal_period, applied_price, len(rates))
    if macd_values is None:
        print(f"Error: No MACD data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['MACD'] = macd_values[0][-len(data):]  # Align with the length of the data
    data['MACD_Signal'] = macd_values[1][-len(data):]  # Align with the length of the data
    data['MACD_Hist'] = macd_values[2][-len(data):]  # Align with the length of the data
    
    # Set NaN MACD values to 0
    data['MACD'].fillna(0, inplace=True)
    data['MACD_Signal'].fillna(0, inplace=True)
    data['MACD_Hist'].fillna(0, inplace=True)
    
    return data