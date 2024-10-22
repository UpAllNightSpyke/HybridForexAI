import MetaTrader5 as mt5
import pandas as pd

# Define the parameters for the MACD indicator
indicator_params = ['fast_period', 'slow_period', 'signal_period', 'applied_price']

def calculate_macd(data, symbol, timeframe, periods={'fast': 12, 'slow': 26, 'signal': 9}):
    print("Calculating MACD using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + periods['slow'])
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get MACD values using MT5 built-in function
    macd_values = mt5.iMACD(symbol, timeframe, periods['fast'], periods['slow'], periods['signal'], mt5.PRICE_CLOSE, len(rates))
    if macd_values is None:
        print(f"Error: No MACD data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['MACD'] = macd_values[0][-len(data):]  # Align with the length of the data
    data['MACD_Signal'] = macd_values[1][-len(data):]  # Align with the length of the data
    
    # Set NaN MACD values to 0
    data['MACD'].fillna(0, inplace=True)
    data['MACD_Signal'].fillna(0, inplace=True)
    
    return data