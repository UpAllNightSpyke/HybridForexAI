import MetaTrader5 as mt5
import pandas as pd

# Define the parameters for the Alligator indicator
indicator_params = ['jaw_period', 'jaw_shift', 'teeth_period', 'teeth_shift', 'lips_period', 'lips_shift']

def calculate_alligator(data, symbol, timeframe, periods={'jaw': 13, 'teeth': 8, 'lips': 5, 'jaw_shift': 8, 'teeth_shift': 5, 'lips_shift': 3}):
    print("Calculating Alligator using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + periods['jaw'])
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get Alligator values using MT5 built-in function
    jaw_values = mt5.iAlligator(symbol, timeframe, periods['jaw'], periods['jaw_shift'], periods['teeth'], periods['teeth_shift'], periods['lips'], periods['lips_shift'], mt5.PRICE_CLOSE, len(rates))
    if jaw_values is None:
        print(f"Error: No Alligator data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['Alligator_Jaw'] = jaw_values[0][-len(data):]  # Align with the length of the data
    data['Alligator_Teeth'] = jaw_values[1][-len(data):]  # Align with the length of the data
    data['Alligator_Lips'] = jaw_values[2][-len(data):]  # Align with the length of the data
    
    # Set NaN Alligator values to 0
    data['Alligator_Jaw'].fillna(0, inplace=True)
    data['Alligator_Teeth'].fillna(0, inplace=True)
    data['Alligator_Lips'].fillna(0, inplace=True)
    
    return data