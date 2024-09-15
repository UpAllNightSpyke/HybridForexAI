// Define the MarketData structure
struct MarketData
{
    datetime time;
    double open;
    double high;
    double low;
    double close;
    long volume;
    double movingAverage;
    double alligatorJaw;
    double alligatorTeeth;
    double alligatorLips;
    double rsi;
};

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
{
    // Array to hold market data
    MarketData marketDataArray[];
    
    // Example data arrays (replace with actual data retrieval)
    MqlRates rates[];
    double ma[];
    double alligatorJaw[];
    double alligatorTeeth[];
    double alligatorLips[];
    double rsi[];
    
    // Retrieve market data (replace with actual data retrieval logic)
    int dataCount = CopyRates(Symbol(), Period(), 0, 1000, rates);
    ArrayResize(ma, dataCount);
    ArrayResize(alligatorJaw, dataCount);
    ArrayResize(alligatorTeeth, dataCount);
    ArrayResize(alligatorLips, dataCount);
    ArrayResize(rsi, dataCount);
    
    // Populate marketDataArray
    for(int i = 0; i < dataCount; i++)
    {
        MarketData data;
        data.time = rates[i].time;
        data.open = rates[i].open;
        data.high = rates[i].high;
        data.low = rates[i].low;
        data.close = rates[i].close;
        data.volume = rates[i].tick_volume;
        data.movingAverage = (i < ArraySize(ma)) ? ma[i] : 0.0;
        data.alligatorJaw = (i < ArraySize(alligatorJaw)) ? alligatorJaw[i] : 0.0;
        data.alligatorTeeth = (i < ArraySize(alligatorTeeth)) ? alligatorTeeth[i] : 0.0;
        data.alligatorLips = (i < ArraySize(alligatorLips)) ? alligatorLips[i] : 0.0;
        data.rsi = (i < ArraySize(rsi)) ? rsi[i] : 0.0;
        ArrayResize(marketDataArray, ArraySize(marketDataArray) + 1);
        marketDataArray[ArraySize(marketDataArray) - 1] = data;
    }

    // Write data to TSV file
    int file_handle = FileOpen("MarketData.tsv", FILE_WRITE|FILE_CSV|FILE_COMMON, "\t");
    if(file_handle != INVALID_HANDLE)
    {
        // Write header
        FileWrite(file_handle, "Time\tOpen\tHigh\tLow\tClose\tVolume\tMovingAverage\tAlligatorJaw\tAlligatorTeeth\tAlligatorLips\tRSI");
        // Write data
        for(int i = 0; i < ArraySize(marketDataArray); i++)
        {
            MarketData data = marketDataArray[i];
            FileWrite(file_handle, TimeToString(data.time, TIME_DATE|TIME_MINUTES), 
                      data.open, data.high, data.low, data.close, data.volume, 
                      data.movingAverage, data.alligatorJaw, data.alligatorTeeth, data.alligatorLips, data.rsi);
        }
        FileClose(file_handle);
        Print("Data written to MarketData.tsv");
    }
    else
    {
        Print("Failed to open file for writing");
    }
}