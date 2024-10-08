import MetaTrader5 as mt5
import pandas as pd

def calculate_rsi(data, symbol, timeframe, period=14):
    print("Calculating RSI using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get RSI values using MT5 built-in function
    rsi_values = mt5.iRSI(symbol, timeframe, period, mt5.PRICE_CLOSE, len(rates))
    if rsi_values is None:
        print(f"Error: No RSI data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['RSI'] = rsi_values[-len(data):]  # Align with the length of the data
    
    # Set NaN RSI values to 0
    data['RSI'].fillna(0, inplace=True)
    
    return data

def calculate_sma(data, symbol, timeframe, period=14):
    print("Calculating SMA using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get SMA values using MT5 built-in function
    sma_values = mt5.iMA(symbol, timeframe, period, 0, mt5.MA_METHOD_SMA, mt5.PRICE_CLOSE, len(rates))
    if sma_values is None:
        print(f"Error: No SMA data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['SMA'] = sma_values[-len(data):]  # Align with the length of the data
    
    # Set NaN SMA values to 0
    data['SMA'].fillna(0, inplace=True)
    
    return data

def calculate_ema(data, symbol, timeframe, period=14):
    print("Calculating EMA using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get EMA values using MT5 built-in function
    ema_values = mt5.iMA(symbol, timeframe, period, 0, mt5.MA_METHOD_EMA, mt5.PRICE_CLOSE, len(rates))
    if ema_values is None:
        print(f"Error: No EMA data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['EMA'] = ema_values[-len(data):]  # Align with the length of the data
    
    # Set NaN EMA values to 0
    data['EMA'].fillna(0, inplace=True)
    
    return data

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

def calculate_alligator(data, symbol, timeframe, periods={'jaw': 13, 'teeth': 8, 'lips': 5, 'jaw_shift': 8, 'teeth_shift': 5, 'lips_shift': 3}):
    print("Calculating Alligator using MT5...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + periods['jaw'])
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    
    # Get Alligator values using MT5 built-in function
    jaw_values = mt5.iAlligator(symbol, timeframe, periods['jaw'], periods['jaw_shift'], periods['teeth'], periods['teeth_shift'], periods['lips'], periods['lips_shift'], mt5.PRICE_CLOSE, len(rates))
    if jaw_values is None:
        print(f"Error: No Alligator data returned for {symbol} on timeframe {timeframe}")
        return data
    
    data['Alligator_Jaw'] = jaw_values[0][-len(data):]  # Align with the length of the data
    data['Alligator_Teeth'] = jaw_values[1][-len(data):]  # Align with the length of the data
    data['Alligator_Lips'] = jaw_values[2][-len(data):]  # Align with the length of the data
    
    # Set NaN Alligator values to 0
    data['Alligator_Jaw'].fillna(0, inplace=True)
    data['Alligator_Teeth'].fillna(0, inplace=True)
    data['Alligator_Lips'].fillna(0, inplace=True)
    
    return data

# Update the indicator_functions dictionary
indicator_functions = {
    'MACD': calculate_macd,
    'Alligator': calculate_alligator,
    'RSI': calculate_rsi,
    'SMA': calculate_sma,
    'EMA': calculate_ema
}

def get_available_indicators():
    return list(indicator_functions.keys())