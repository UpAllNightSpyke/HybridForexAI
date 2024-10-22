import pandas as pd
from .indicator_library import AppliedPrice

# Define the parameters for the RSI indicator
indicator_params = ['period', 'applied_price']

def calculate_rsi(data, symbol, timeframe, params):
    print("Calculating RSI using custom function...")
    period = int(params.get('period', 14))
    applied_price = params.get('applied_price', 'close').lower()  # Ensure lowercase
    overbought = int(params.get('overbought', 70))
    oversold = int(params.get('oversold', 30))

    # Ensure DataFrame column names are in lowercase
    data.columns = map(str.lower, data.columns)

    if applied_price not in data.columns:
        raise ValueError(f"Applied price '{applied_price}' not found in data columns")

    # Calculate RSI
    delta = data[applied_price].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi_df = pd.DataFrame(index=data.index)
    rsi_df['RSI'] = 100 - (100 / (1 + rs))

    # Set NaN RSI values to 0
    rsi_df.fillna(0, inplace=True)

    # Add signals for overbought and oversold
    rsi_df['RSI_Signal'] = 0
    rsi_df.loc[rsi_df['RSI'] > overbought, 'RSI_Signal'] = 1
    rsi_df.loc[rsi_df['RSI'] < oversold, 'RSI_Signal'] = -1
    
    return rsi_df

# Example usage
if __name__ == "__main__":
    # Load your data
    data = pd.read_csv('your_data.csv')  # Replace with your data source

    # Define parameters
    params = {'period': 14, 'applied_price': 'close'}

    # Calculate RSI
    rsi_df = calculate_rsi(data, 'AAPL', 'daily', params)

    # Print the RSI DataFrame
    print(rsi_df)

    # # Plotting (optional)
    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(10, 5))
    # plt.plot(rsi_df['RSI'], label='RSI')
    # plt.axhline(70, color='red', linestyle='--', label='Overbought')
    # plt.axhline(30, color='green', linestyle='--', label='Oversold')
    # plt.legend()
    # plt.show()