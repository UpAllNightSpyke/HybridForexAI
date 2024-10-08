import pandas as pd
from indicators import get_available_indicators

def format_data(input_file, output_file):
    # Load data from CSV with tab delimiter
    data = pd.read_csv(input_file, delimiter='\t')
    print(f"Columns in the input data: {data.columns.tolist()}")
    
    # Define the required columns based on possible indicators
    possible_columns = {
        'time': 'Time',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'tick_volume': 'Volume'
    }
    
    # Add available indicators to possible columns
    available_indicators = get_available_indicators()
    for indicator in available_indicators:
        possible_columns[indicator] = indicator
    
    # Check for missing columns and raise an error if any required columns are missing
    required_columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"'{col}' column is missing from the data")
    
    # Remove the 'real_volume' column if it exists
    if 'real_volume' in data.columns:
        data.drop(columns=['real_volume'], inplace=True)
    
    # Save the formatted data to TSV
    data.to_csv(output_file, sep='\t', index=False)

    print(f"Formatted data saved to {output_file}")