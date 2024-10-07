import pandas as pd
from indicators.functions import initialize_indicators, get_available_indicators
import os
import re
import warnings

def remove_nan_rows(data, indicator_columns):
    # Remove rows where any of the indicator columns have NaN values
    data = data.dropna(subset=indicator_columns)
    return data

def extract_symbol_timeframe(filename):
    match = re.match(r"([A-Z]+)_(\d+)\.csv", filename)
    if match:
        symbol, timeframe = match.groups()
        return symbol, timeframe
    else:
        warnings.warn(f"Filename {filename} does not match the expected pattern.")
        return None, None

if __name__ == "__main__":
    # Initialize indicators to get the parameters
    initialize_indicators()
    _, indicator_params = get_available_indicators()

    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the input and output directories using the absolute path
    input_dir = os.path.join(script_dir, 'data', 'raw')
    output_dir = os.path.join(script_dir, 'data', 'cleaned')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            symbol, timeframe = extract_symbol_timeframe(filename)
            if symbol and timeframe:
                try:
                    print(f"Processing file: {filename} with symbol: {symbol} and timeframe: {timeframe}")

                    # Construct the input file path
                    input_file = os.path.join(input_dir, filename)
                    
                    # Load your data from the CSV file
                    data = pd.read_csv(input_file)

                    # Print the columns of the DataFrame for debugging
                    print(f"Columns in the input data: {data.columns.tolist()}")

                    # Get the actual indicator columns to be cleaned, excluding 'RSI_Signal'
                    indicator_columns = [col for col in data.columns if col not in ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume', 'RSI_Signal']]

                    # Print the indicator columns for debugging
                    print(f"Indicator columns to be cleaned: {indicator_columns}")

                    # Remove rows with NaN values in the indicator columns
                    cleaned_data = remove_nan_rows(data, indicator_columns)

                    # Construct the output file path
                    output_file = os.path.join(output_dir, f"{symbol}_{timeframe}_cleaned.csv")
                    
                    # Save the cleaned data to a new CSV file
                    cleaned_data.to_csv(output_file, index=False)
                    print(f"Cleaned data saved to {output_file}")
                except ValueError as e:
                    print(e)