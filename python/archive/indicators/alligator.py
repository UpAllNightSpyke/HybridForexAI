import MetaTrader5 as mt5
import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the Alligator indicator
indicator_params = ['jaw_period', 'jaw_shift', 'teeth_period', 'teeth_shift', 'lips_period', 'lips_shift', 'applied_price']

def calculate_alligator(data, symbol, timeframe, params):
    print("Calculating Alligator using MT5...")
    jaw_period = int(params.get('jaw_period', 13))
    jaw_shift = int(params.get('jaw_shift', 8))
    teeth_period = int(params.get('teeth_period', 8))
    teeth_shift = int(params.get('teeth_shift', 5))
    lips_period = int(params.get('lips_period', 5))
    lips_shift = int(params.get('lips_shift', 3))
    applied_price = AppliedPrice[params.get('applied_price', 'CLOSE')].value

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + jaw_period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get Alligator values using MT5 built-in function
    jaw_values = mt5.iAlligator(symbol, timeframe, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift, applied_price, len(rates))
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