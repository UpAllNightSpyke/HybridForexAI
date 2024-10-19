import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from appdirs import user_data_dir
import re

def normalize_data():
    """Normalizes the cleaned data using Min-Max scaling.

    Reads the symbol and timeframe from the filename of the cleaned data.

    Returns:
        pd.DataFrame: The normalized DataFrame, or None if an error occurs.
    """

    # Get the user data directory
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")

    # Define the input and output directories within the user data directory
    input_dir = os.path.join(user_data_path, 'forex_data', 'cleaned')
    output_dir = os.path.join(user_data_path, 'forex_data', 'normalized')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Find the cleaned data file
        for filename in os.listdir(input_dir):
            if filename.endswith("_cleaned.csv"):
                input_file = os.path.join(input_dir, filename)
                break  # Assume only one cleaned file exists
        else:
            print("Error: No cleaned data file found in the input directory.")
            return None

        # Extract symbol and timeframe from filename
        match = re.match(r"(.+)_(\w+)_cleaned\.csv", filename)
        if match:
            symbol, timeframe = match.groups()
        else:
            print(f"Error: Could not extract symbol and timeframe from filename: {filename}")
            return None

        # Construct the output file path
        output_file = os.path.join(output_dir, f"{symbol}_{timeframe}_normalized.csv")

        # Load the cleaned data
        data = pd.read_csv(input_file)

        # Select the columns to normalize (exclude 'time' and any non-numeric columns)
        cols_to_normalize = [col for col in data.columns if col != 'time' and data[col].dtype in ['int64', 'float64']]

        # Create a MinMaxScaler instance
        scaler = MinMaxScaler()

        # Fit and transform the selected columns
        data[cols_to_normalize] = scaler.fit_transform(data[cols_to_normalize])

        # Save the normalized data
        data.to_csv(output_file, index=False)
        print(f"Normalized data saved to {output_file}")

        return data

    except Exception as e:
        print(f"Error normalizing data: {e}")
        return None
