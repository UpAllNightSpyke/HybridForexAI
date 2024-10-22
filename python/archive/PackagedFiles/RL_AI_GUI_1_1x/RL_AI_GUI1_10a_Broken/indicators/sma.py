import MetaTrader5 as mt5
import pandas as pd

# Define the parameters for the SMA indicator
indicator_params = ['period', 'shift', 'method', 'applied_price']

def calculate_sma(data, symbol, timeframe, period=14):
    print("Calculating SMA using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get SMA values using MT5 built-in function
    sma_values = mt5.iMA(symbol, timeframe, period, 0, mt5.MA_METHOD_SMA, mt5.PRICE_CLOSE, len(rates))
    if sma_values is None:
        print(f"Error: No SMA data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['SMA'] = sma_values[-len(data):]  # Align with the length of the data
    
    # Set NaN SMA values to 0
    data['SMA'].fillna(0, inplace=True)
    
    return data