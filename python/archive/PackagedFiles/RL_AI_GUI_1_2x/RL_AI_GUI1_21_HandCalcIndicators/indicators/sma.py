import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the SMA indicator
indicator_params = ['period', 'shift', 'applied_price']

def calculate_sma(data, symbol, timeframe, params):
    print("Calculating SMA using custom function...")
    period = int(params.get('period', 14))
    shift = int(params.get('shift', 0))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate SMA
    sma_df = pd.DataFrame(index=data.index)
    sma_df['SMA'] = data[applied_price].rolling(window=period).mean().shift(shift)

    # Set NaN SMA values to 0
    sma_df.fillna(0, inplace=True)
    
    return sma_df