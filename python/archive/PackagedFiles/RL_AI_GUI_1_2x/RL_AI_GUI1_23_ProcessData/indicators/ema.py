import pandas as pd
from .indicator_library import AppliedPrice, Method

# Define the parameters for the EMA indicator
indicator_params = ['period', 'shift', 'method', 'applied_price']

def calculate_ema(data, symbol, timeframe, params):
    print("Calculating EMA using custom function...")
    period = int(params.get('period', 14))
    shift = int(params.get('shift', 0))
    method = params.get('method', 'EMA')
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    if method != 'EMA':
        print(f"Error: Unsupported method {method} for EMA calculation.")
        return data

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate EMA
    ema_df = pd.DataFrame(index=data.index)
    ema_df['EMA'] = data[applied_price].ewm(span=period, adjust=False).mean().shift(shift)

    # # Set NaN EMA values to 0
    # ema_df.fillna(0, inplace=True)
    
    return ema_df