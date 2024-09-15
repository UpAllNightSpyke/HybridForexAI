//+------------------------------------------------------------------+
//|                                               DataScript.mq5 |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                 https://www.upallnightspyke.com/ |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.upallnightspyke.com/"
#property version   "1.00"

//+------------------------------------------------------------------+
//| Data Collection to be used in a RL neural network. Processed     |
//| through python code and used in a c++ model                      |
//+------------------------------------------------------------------+

// Global variables to accept parameters
int BarsToRetrieve = 100; // Default value
ENUM_TIMEFRAMES Timeframe = PERIOD_H1; // Default value
int MovingAveragePeriod = 14; // Default value

struct MarketData
{
    datetime time;
    double open;
    double high;
    double low;
    double close;
    long volume; // Changed to long to match MqlRates.tick_volume
    double indicator; // Indicator data at the end
};

void OnStart()
{
    // Retrieve parameters from global variables
    if (GlobalVariableCheck("BarsToRetrieve"))
        BarsToRetrieve = GlobalVariableGet("BarsToRetrieve");
    if (GlobalVariableCheck("Timeframe"))
        Timeframe = (ENUM_TIMEFRAMES)GlobalVariableGet("Timeframe");
    if (GlobalVariableCheck("MovingAveragePeriod"))
        MovingAveragePeriod = GlobalVariableGet("MovingAveragePeriod");

    // Print debug information
    Print("BarsToRetrieve: ", BarsToRetrieve);
    Print("Timeframe: ", Timeframe);
    Print("MovingAveragePeriod: ", MovingAveragePeriod);

    // Validate parameters
    if (BarsToRetrieve <= 0 || MovingAveragePeriod <= 0)
    {
        Print("Invalid parameters: BarsToRetrieve or MovingAveragePeriod is less than or equal to 0");
        return;
    }

    // Retrieve and combine data
    MarketData marketDataArray[];
    double ma[];
    MqlRates rates[];
    ArraySetAsSeries(ma, true);
    ArraySetAsSeries(rates, true);
    int copiedRates = CopyRates(Symbol(), Timeframe, 0, BarsToRetrieve, rates);
    
    if (copiedRates <= 0)
    {
        Print("Failed to copy rates");
        return;
    }

    // Get the handle to the moving average indicator
    int maHandle = iMA(Symbol(), Timeframe, MovingAveragePeriod, 0, MODE_SMA, PRICE_CLOSE);
    if (maHandle == INVALID_HANDLE)
    {
        Print("Failed to create moving average handle");
        return;
    }

    // Copy the moving average values into the ma array
    int copiedMA = CopyBuffer(maHandle, 0, 0, BarsToRetrieve, ma);
    if (copiedMA <= 0)
    {
        Print("Failed to copy moving average values");
        return;
    }

    for(int i = 0; i < copiedRates; i++)
    {
        MarketData data;
        data.time = rates[i].time;
        data.open = rates[i].open;
        data.high = rates[i].high;
        data.low = rates[i].low;
        data.close = rates[i].close;
        data.volume = rates[i].tick_volume; // No conversion needed
        data.indicator = (i < ArraySize(ma)) ? ma[i] : 0.0;
        ArrayResize(marketDataArray, ArraySize(marketDataArray) + 1);
        marketDataArray[ArraySize(marketDataArray) - 1] = data;
    }

    // Write data to CSV file
    int file_handle = FileOpen("MarketData.csv", FILE_WRITE|FILE_CSV|FILE_COMMON);
    if(file_handle != INVALID_HANDLE)
    {
        FileWrite(file_handle, "Time,Open,High,Low,Close,Volume,Indicator");
        for(int i = 0; i < ArraySize(marketDataArray); i++)
        {
            MarketData data = marketDataArray[i];
            FileWrite(file_handle, TimeToString(data.time, TIME_DATE|TIME_MINUTES), 
                      data.open, data.high, data.low, data.close, data.volume, data.indicator);
        }
        FileClose(file_handle);
        Print("Data written to MarketData.csv");
    }
    else
    {
        Print("Failed to open file for writing");
    }
}