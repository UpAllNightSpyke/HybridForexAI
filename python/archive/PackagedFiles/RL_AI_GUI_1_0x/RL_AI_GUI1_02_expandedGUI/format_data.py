import pandas as pd

def format_data(input_file, output_file):
    # Load data from CSV
    data = pd.read_csv(input_file)
    print(f"Columns in the input data: {data.columns.tolist()}")
    
    # Define the required columns based on possible indicators
    possible_columns = {
        'time': 'Time',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'tick_volume': 'Volume',
        'RSI': 'RSI',
        'Alligator_Jaw': 'AlligatorJaw',
        'Alligator_Teeth': 'AlligatorTeeth',
        'Alligator_Lips': 'AlligatorLips',
        'SMA': 'SMA',
        'EMA': 'EMA',
        'MACD': 'MACD'
    }
    
    # Check for missing columns and raise an error if any required columns are missing
    required_columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"'{col}' column is missing from the data")
    
    # Remove the 'real_volume' column if it exists
    if 'real_volume' in data.columns:
        data = data.drop(columns=['real_volume'])
    
    # Rename columns to match the desired output
    rename_columns = {col: new_col for col, new_col in possible_columns.items() if col in data.columns}
    data.rename(columns=rename_columns, inplace=True)
    print(f"Columns in the renamed data: {data.columns.tolist()}")
    
    # Save to TSV file
    data.to_csv(output_file, sep='\t', index=False)
    print(f"Data written to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python format_data.py <input_file> <output_file>")
    else:
        format_data(sys.argv[1], sys.argv[2])