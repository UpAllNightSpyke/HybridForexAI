import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the RSI indicator
indicator_params = ['period', 'applied_price']

def calculate_rsi(data, symbol, timeframe, params):
    print("Calculating RSI using custom function...")
    period = int(params.get('period', 14))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate RSI
    delta = data[applied_price].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi_df = pd.DataFrame(index=data.index)
    rsi_df['RSI'] = 100 - (100 / (1 + rs))

    # Set NaN RSI values to 0
    rsi_df.fillna(0, inplace=True)
    
    return rsi_df