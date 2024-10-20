import pandas as pd
from indicators.functions import initialize_indicators, get_available_indicators
import os
import re
import warnings
import sys
from datetime import datetime
from indicators.indicator_library import Timeframe, TIMEFRAME_MAP
from tkinter import messagebox
from appdirs import user_data_dir  # Import user_data_dir

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

def process_data(symbol, timeframe):
    try:
        # Initialize indicators to get the parameters
        initialize_indicators()
        _, indicator_params = get_available_indicators()

        # --- Modified Section ---
        # Get the user data directory
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")  # Adjust app_name and author if needed

        # Define the input and output directories within the user data directory
        input_dir = os.path.join(user_data_path, 'forex_data', 'raw')
        output_dir = os.path.join(user_data_path, 'forex_data', 'cleaned')

        # Ensure the input and output directories exist
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        # Construct the input file path using the user data directory
        input_file = os.path.join(input_dir, f"{symbol}_{timeframe}.csv")
        # --- End of Modified Section ---

        # Load your data from the CSV file
        data = pd.read_csv(input_file)

        # Convert 'time' column to datetime objects
        data['time'] = pd.to_datetime(data['time'])

        # Convert datetime objects to numerical timestamps (seconds since epoch)
        data['time'] = data['time'].astype('int64') // 10**9  

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
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: preprocess_data.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]

    process_data(symbol, timeframe)