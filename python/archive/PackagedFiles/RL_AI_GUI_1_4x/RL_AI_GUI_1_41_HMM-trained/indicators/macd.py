import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the MACD indicator
indicator_params = ['fast_period', 'slow_period', 'signal_period', 'applied_price']

def calculate_macd(data, symbol, timeframe, params):
    print("Calculating MACD using custom function...")
    fast_period = int(params.get('fast_period', 12))
    slow_period = int(params.get('slow_period', 26))
    signal_period = int(params.get('signal_period', 9))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate MACD
    macd_df = pd.DataFrame(index=data.index)
    macd_df['MACD_Line'] = data[applied_price].ewm(span=fast_period, adjust=False).mean() - data[applied_price].ewm(span=slow_period, adjust=False).mean()
    macd_df['Signal_Line'] = macd_df['MACD_Line'].ewm(span=signal_period, adjust=False).mean()
    macd_df['MACD_Histogram'] = macd_df['MACD_Line'] - macd_df['Signal_Line']

    # # Set NaN MACD values to 0
    # macd_df.fillna(0, inplace=True)
    
    return macd_df