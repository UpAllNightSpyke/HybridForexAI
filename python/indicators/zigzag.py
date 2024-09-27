import MetaTrader5 as mt5
import pandas as pd
from .indicator_library import Method

# Define the parameters for the ZigZag indicator
indicator_params = ['depth', 'deviation', 'backstep', 'method']

def calculate_zigzag(data, symbol, timeframe, params):
    print("Calculating ZigZag using MT5...")
    depth = int(params.get('depth', 12))
    deviation = float(params.get('deviation', 5.0))
    backstep = int(params.get('backstep', 3))
    method = Method[params.get('method', 'SMA')].value

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + depth)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get ZigZag values using MT5 built-in function
    zigzag_values = mt5.iCustom(symbol, timeframe, 'ZigZag', depth, deviation, backstep, method, len(rates))
    if zigzag_values is None:
        print(f"Error: No ZigZag data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['ZigZag'] = zigzag_values[-len(data):]  # Align with the length of the data
    
    # Set NaN ZigZag values to 0
    data['ZigZag'].fillna(0, inplace=True)
    
    return data