import os
from datetime import datetime
from MT5_scraper import scrape_mt5_data
from format_data import format_data
from train_rl_agent import main as train_rl_agent_main
import MetaTrader5 as mt5
from indicators import get_available_indicators  # Updated import

def main(symbol='XAUUSD', timeframe=mt5.TIMEFRAME_H1, start_date=datetime(2022, 1, 1), end_date=datetime(2022, 12, 31), account=3021640, password='AItester1!', server='PlexyTrade-Server01', mt5_path='', indicators=None, indicator_periods=None):
    if indicators is None:
        indicators = get_available_indicators()
    
    if indicator_periods is None:
        # Default periods if not provided
        indicator_periods = {'RSI': 14, 'SMA': 30, 'EMA': 20}
    
    print(f"Selected indicators: {indicators}")
    print(f"Indicator periods: {indicator_periods}")
    
    raw_output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'MarketData.csv')
    formatted_output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'processed', 'MarketData_Prepared.tsv')
    
    # Ensure the directories exist
    os.makedirs(os.path.dirname(raw_output_file), exist_ok=True)
    os.makedirs(os.path.dirname(formatted_output_file), exist_ok=True)
    
    # Step 1: Scrape data from MT5
    scrape_mt5_data(symbol, timeframe, start_date, end_date, raw_output_file, account, password, server, mt5_path, indicators, indicator_periods)
    
    # Step 2: Format the scraped data
    format_data(raw_output_file, formatted_output_file)
    
    # Step 3: Train the RL agent
    train_rl_agent_main()

if __name__ == "__main__":
    main()