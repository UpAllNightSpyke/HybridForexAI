import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the Zigzag indicator
indicator_params = ['depth', 'deviation', 'backstep', 'applied_price']

def calculate_zigzag(data, symbol, timeframe, params):
    print("Calculating Zigzag using custom function...")
    depth = int(params.get('depth', 12))
    deviation = float(params.get('deviation', 5.0))
    backstep = int(params.get('backstep', 3))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Placeholder for Zigzag calculation (implement actual Zigzag logic here)
    zigzag_df = pd.DataFrame(index=data.index)
    zigzag_df['Zigzag'] = data[applied_price]  # This is a placeholder, replace with actual Zigzag calculation

    # # Set NaN Zigzag values to 0
    # zigzag_df.fillna(0, inplace=True)
    
    return zigzag_df