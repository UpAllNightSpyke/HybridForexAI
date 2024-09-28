import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the Alligator indicator
indicator_params = ['jaw_period', 'jaw_shift', 'teeth_period', 'teeth_shift', 'lips_period', 'lips_shift', 'applied_price']

def calculate_alligator(data, symbol, timeframe, params):
    print("Calculating Alligator using custom function...")
    jaw_period = int(params.get('jaw_period', 13))
    jaw_shift = int(params.get('jaw_shift', 8))
    teeth_period = int(params.get('teeth_period', 8))
    teeth_shift = int(params.get('teeth_shift', 5))
    lips_period = int(params.get('lips_period', 5))
    lips_shift = int(params.get('lips_shift', 3))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate Alligator indicator
    alligator_df = pd.DataFrame(index=data.index)
    alligator_df['Alligator_Jaw'] = data[applied_price].rolling(window=jaw_period).mean().shift(jaw_shift)
    alligator_df['Alligator_Teeth'] = data[applied_price].rolling(window=teeth_period).mean().shift(teeth_shift)
    alligator_df['Alligator_Lips'] = data[applied_price].rolling(window=lips_period).mean().shift(lips_shift)

    # # Set NaN Alligator values to 0
    # alligator_df.fillna(0, inplace=True)
    
    return alligator_df