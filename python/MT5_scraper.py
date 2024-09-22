# Step 1: Install MetaTrader 5 package
# pip install MetaTrader5

# Step 2: Import necessary libraries
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib
import subprocess

# Step 3: Connect to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# Step 4: Define functions to retrieve historical data and calculate indicators
def get_historical_data(symbol, timeframe, start, end):
    rates = mt5.copy_rates_range(symbol, timeframe, start, end)
    if rates is None:
        print(f"Failed to retrieve data for {symbol}")
        return None
    return pd.DataFrame(rates)

def calculate_indicators(data):
    data['movingAverage'] = talib.SMA(data['close'], timeperiod=14)
    data['alligatorJaw'] = talib.SMA(data['close'], timeperiod=13)
    data['alligatorTeeth'] = talib.SMA(data['close'], timeperiod=8)
    data['alligatorLips'] = talib.SMA(data['close'], timeperiod=5)
    data['rsi'] = talib.RSI(data['close'], timeperiod=14)
    return data

# Step 5: Retrieve and save data in CSV format
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1
start = pd.Timestamp('2022-01-01')
end = pd.Timestamp('2022-12-31')

data = get_historical_data(symbol, timeframe, start, end)
if data is not None:
    data = calculate_indicators(data)
    csv_file_path = './data/processed/MarketData_Prepared.csv'
    data.to_csv(csv_file_path, index=False)
    print("Data saved successfully in CSV format.")

# Shutdown MetaTrader 5 connection
mt5.shutdown()

# Step 6: Process the CSV file using data_preparation.py
subprocess.run(['python', 'data_preparation.py', csv_file_path])

# Step 7: Load the prepared data for training
import train_rl_agent

if __name__ == "__main__":
    train_rl_agent.main()