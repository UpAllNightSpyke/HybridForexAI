import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_tsv(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame
    
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        if raw_data.startswith(b'\xef\xbb\xbf'):
            encoding = 'utf-8-sig'
        elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
            encoding = 'utf-16'
        else:
            encoding = 'latin1'
    
    data = pd.read_csv(file_path, encoding=encoding, delimiter='\t')
    print(f"Successfully loaded TSV with encoding: {encoding}")
    return data

def prepare_data(data):
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']
    
    data['AlligatorJaw'] = data['AlligatorJaw'].replace({0: pd.NA})
    data['AlligatorTeeth'] = data['AlligatorTeeth'].replace({0: pd.NA})
    data['AlligatorLips'] = data['AlligatorLips'].replace({0: pd.NA})
    data['RSI'] = data['RSI'].replace({0: pd.NA})
    data['AlligatorJaw'] = data['AlligatorJaw'].fillna(data['AlligatorJaw'].mean())
    data['AlligatorTeeth'] = data['AlligatorTeeth'].fillna(data['AlligatorTeeth'].mean())
    data['AlligatorLips'] = data['AlligatorLips'].fillna(data['AlligatorLips'].mean())
    data['RSI'] = data['RSI'].fillna(data['RSI'].mean())

    scaler = MinMaxScaler()
    data[features] = scaler.fit_transform(data[features])

    print("Min values after normalization:")
    print(data[features].min())
    print("Max values after normalization:")
    print(data[features].max())

    return data

def main():
    file_path = os.path.join(os.getcwd(), 'DataCollection', 'TestData', 'MarketData_LastWeek.tsv')
    print(f"Loading data from: {file_path}")
    data = load_tsv(file_path)

    # Debugging: Print the first few rows of the loaded data
    print("First few rows of the loaded data:")
    print(data.head())

    if data.empty:
        print("The DataFrame is empty. Please check the file content and path.")
        return

    data = prepare_data(data)
    prepared_file_path = os.path.join(os.getcwd(), 'ModelCreate', 'Models', 'PreparedModelData.tsv')
    data.to_csv(prepared_file_path, sep='\t', index=False)
    print(f"Data preparation complete. Prepared data saved to '{prepared_file_path}'.")

if __name__ == "__main__":
    main()