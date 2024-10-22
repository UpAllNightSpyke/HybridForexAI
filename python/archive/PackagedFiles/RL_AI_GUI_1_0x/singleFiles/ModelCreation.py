import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Function to read the TSV file and handle BOM
def load_tsv(file_path):
    with open(file_path, 'rb') as file:
        # Read the first few bytes to check for BOM
        raw_data = file.read()
        if raw_data.startswith(b'\xef\xbb\xbf'):
            # UTF-8 BOM detected
            encoding = 'utf-8-sig'
        elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
            # UTF-16 BOM detected
            encoding = 'utf-16'
        else:
            # Default to latin1 if no BOM detected
            encoding = 'latin1'
    
    # Read the TSV file with the detected encoding
    data = pd.read_csv(file_path, encoding=encoding, delimiter='\t')
    print(f"Successfully loaded TSV with encoding: {encoding}")
    return data

# Use an absolute path to the TSV file
file_path = os.path.join(os.getcwd(), 'DataCollection', 'TestData', 'MarketData_LastWeek.tsv')

# Load the TSV file with the correct file path
data = load_tsv(file_path)

# Display the first few rows of the DataFrame
print(data.head())

# Print the column names to debug the issue
print("Column names:", data.columns)

# Select the features to normalize (excluding 'Time')
features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']

# Check if the expected columns are in the DataFrame
missing_columns = [feature for feature in features if feature not in data.columns]
if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    # Print original values of 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', and 'RSI' columns
    print("Original 'AlligatorJaw' values:")
    print(data['AlligatorJaw'].head(10))
    print("Original 'AlligatorTeeth' values:")
    print(data['AlligatorTeeth'].head(10))
    print("Original 'AlligatorLips' values:")
    print(data['AlligatorLips'].head(10))
    print("Original 'RSI' values:")
    print(data['RSI'].head(10))

    # Print min and max values before normalization
    print("Min values before normalization:")
    print(data[features].min())
    print("Max values before normalization:")
    print(data[features].max())

    # Replace extremely small values with NaN and then fill with the mean of the column
    data['AlligatorJaw'].replace({0: pd.NA}, inplace=True)
    data['AlligatorTeeth'].replace({0: pd.NA}, inplace=True)
    data['AlligatorLips'].replace({0: pd.NA}, inplace=True)
    data['RSI'].replace({0: pd.NA}, inplace=True)
    data['AlligatorJaw'].fillna(data['AlligatorJaw'].mean(), inplace=True)
    data['AlligatorTeeth'].fillna(data['AlligatorTeeth'].mean(), inplace=True)
    data['AlligatorLips'].fillna(data['AlligatorLips'].mean(), inplace=True)
    data['RSI'].fillna(data['RSI'].mean(), inplace=True)

    # Initialize the scaler
    scaler = MinMaxScaler()

    # Fit and transform the data
    data[features] = scaler.fit_transform(data[features])

    # Print min and max values after normalization
    print("Min values after normalization:")
    print(data[features].min())
    print("Max values after normalization:")
    print(data[features].max())

    # Display the first few rows of the normalized DataFrame
    print(data.head())