import MetaTrader5 as mt5
import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the RSI indicator
indicator_params = ['period', 'applied_price']

def calculate_rsi(data, symbol, timeframe, params):
    print("Calculating RSI using MT5...")
    period = int(params.get('period', 14))
    applied_price = AppliedPrice[params.get('applied_price', 'CLOSE')].value

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get RSI values using MT5 built-in function
    rsi_values = mt5.iRSI(symbol, timeframe, period, applied_price, len(rates))
    if rsi_values is None:
        print(f"Error: No RSI data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['RSI'] = rsi_values[-len(data):]  # Align with the length of the data
    
    # Set NaN RSI values to 0
    data['RSI'].fillna(0, inplace=True)
    
    return data