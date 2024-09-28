from enum import Enum
import MetaTrader5 as mt5

# Define enums for different indicators
class AppliedPrice(Enum):
    CLOSE = 0
    OPEN = 1
    HIGH = 2
    LOW = 3
    MEDIAN = 4
    TYPICAL = 5
    WEIGHTED = 6

class Method(Enum):
    SMA = 0
    EMA = 1
    SMMA = 2
    LWMA = 3

class Timeframe(Enum):
    M1 = 1
    M5 = 5
    M15 = 15
    M30 = 30
    H1 = 60
    H4 = 240
    D1 = 1440
    W1 = 10080
    MN1 = 43200

# Map Timeframe enum to MetaTrader 5 constants
TIMEFRAME_MAP = {
    Timeframe.M1: mt5.TIMEFRAME_M1,
    Timeframe.M5: mt5.TIMEFRAME_M5,
    Timeframe.M15: mt5.TIMEFRAME_M15,
    Timeframe.M30: mt5.TIMEFRAME_M30,
    Timeframe.H1: mt5.TIMEFRAME_H1,
    Timeframe.H4: mt5.TIMEFRAME_H4,
    Timeframe.D1: mt5.TIMEFRAME_D1,
    Timeframe.W1: mt5.TIMEFRAME_W1,
    Timeframe.MN1: mt5.TIMEFRAME_MN1
}

# Define input handling functions for non-integer variables
def get_ema_params(params):
    return {
        'period': int(params.get('period', 14)),
        'shift': int(params.get('shift', 0)),
        'method': Method[params.get('method', 'EMA')].value,
        'applied_price': AppliedPrice[params.get('applied_price', 'CLOSE')].value
    }

# Add more input handling functions for other indicators as needed