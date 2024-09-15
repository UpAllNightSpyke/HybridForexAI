import pandas as pd

# Load the CSV file
data = pd.read_csv('DataCollection\TestData\MarketData.csv')

# Display the first few rows of the DataFrame
print(data.head())
from sklearn.preprocessing import MinMaxScaler

# Select the features to normalize
features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']

# Initialize the scaler
scaler = MinMaxScaler()

# Fit and transform the data
data[features] = scaler.fit_transform(data[features])

# Display the first few rows of the normalized DataFrame
print(data.head())