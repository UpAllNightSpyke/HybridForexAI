import pandas as pd
from indicators.functions import initialize_indicators, get_available_indicators

def remove_zero_rows(data, indicator_columns):
    # Remove rows where any of the indicator columns have zeros
    data = data[(data[indicator_columns] != 0).all(axis=1)]
    return data

if __name__ == "__main__":
    # Initialize indicators to get the parameters
    initialize_indicators()
    _, indicator_params = get_available_indicators()

    # Load your data from a CSV file
    input_file = 'data/raw/XAUUSD_30_20240909_20240913.csv'  # Replace with your input file path
    data = pd.read_csv(input_file)

    # Print the columns of the DataFrame for debugging
    print(f"Columns in the input data: {data.columns.tolist()}")

    # Get the actual indicator columns to be cleaned, excluding 'RSI_Signal'
    indicator_columns = [col for col in data.columns if col not in ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume', 'RSI_Signal']]

    # Print the indicator columns for debugging
    print(f"Indicator columns to be cleaned: {indicator_columns}")

    # Remove rows with zeros in the indicator columns
    cleaned_data = remove_zero_rows(data, indicator_columns)

    # Save the cleaned data to a new TSV file
    output_file = 'data/cleaned/XAUUSD_30_20240909_20240913_cleaned.tsv'  # Replace with your output file path
    cleaned_data.to_csv(output_file, sep='\t', index=False)
    print(f"Cleaned data saved to {output_file}")