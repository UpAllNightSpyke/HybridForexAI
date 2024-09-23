import os
from datetime import datetime
from MT5_scraper import scrape_mt5_data
from process_prepare import main as process_prepare_main
import MetaTrader5 as mt5

def main():
    # Define parameters for scraping data
    symbol = 'XAUUSD'
    timeframe = mt5.TIMEFRAME_H1
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'MarketData.csv')
    
    # Step 1: Scrape data from MT5
    scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file)
    
    # Step 2: Process and prepare the scraped data
    process_prepare_main(output_file)

if __name__ == "__main__":
    main()