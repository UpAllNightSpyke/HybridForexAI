import MetaTrader5 as mt5
import pandas as pd

def calculate_indicators(data, symbol, timeframe, indicators, indicator_periods):
    if 'RSI' in indicators:
        data = calculate_rsi(data, symbol, timeframe, period=indicator_periods['RSI'])
    if 'SMA' in indicators:
        data = calculate_sma(data, symbol, timeframe, period=indicator_periods['SMA'])
    if 'EMA' in indicators:
        data = calculate_ema(data, symbol, timeframe, period=indicator_periods['EMA'])
    # Add other indicators as needed
    return data

def calculate_rsi(data, symbol, timeframe, period=14):
    print("Calculating RSI...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    close_prices = pd.Series([rate['close'] for rate in rates])
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Set NaN RSI values to 0
    data['RSI'].fillna(0, inplace=True)
    
    return data

def calculate_sma(data, symbol, timeframe, period=14):
    print("Calculating SMA...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    close_prices = pd.Series([rate['close'] for rate in rates])
    data['SMA'] = close_prices.rolling(window=period).mean()
    
    # Set NaN SMA values to 0
    data['SMA'].fillna(0, inplace=True)
    
    return data

def calculate_ema(data, symbol, timeframe, period=14):
    print("Calculating EMA...")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + period)
    if rates is None:
        print(f"Error: No rates data returned for {symbol} on timeframe {timeframe}")
        return data
    close_prices = pd.Series([rate['close'] for rate in rates])
    data['EMA'] = close_prices.ewm(span=period, adjust=False).mean()
    
    # Set NaN EMA values to 0
    data['EMA'].fillna(0, inplace=True)
    
    return data

def calculate_macd(data, symbol, timeframe):
    macd = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data))
    data['MACD'] = [rate['close'] for rate in macd]
    return data

def calculate_alligator(data, symbol, timeframe):
    jaw_period = 13
    teeth_period = 8
    lips_period = 5
    jaw_shift = 8
    teeth_shift = 5
    lips_shift = 3
    
    jaw = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + jaw_shift)
    teeth = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + teeth_shift)
    lips = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + lips_shift)
    
    data['Alligator_Jaw'] = [rate['close'] for rate in jaw[jaw_shift:]]
    data['Alligator_Teeth'] = [rate['close'] for rate in teeth[teeth_shift:]]
    data['Alligator_Lips'] = [rate['close'] for rate in lips[lips_shift:]]
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