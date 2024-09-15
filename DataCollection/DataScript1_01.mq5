//+------------------------------------------------------------------+
//|                                               DataScript1_01.mq5 |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                 https://www.upallnightspyke.com/ |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.upallnightspyke.com/"
#property version   "1.01"

//+------------------------------------------------------------------+
//| Data Collection to be used in a RL neural network. Processed     |
//| through python code and used in a c++ model                      |
//+------------------------------------------------------------------+

// Global variables to accept parameters
int BarsToRetrieve = 100; // Default value for the number of bars to retrieve
ENUM_TIMEFRAMES Timeframe = PERIOD_H1; // Default value for the timeframe
int MovingAveragePeriod = 14; // Default value for the moving average period

// Alligator input parameters
int JawPeriod = 13; // Default period for the Alligator Jaw
int JawShift = 8; // Default shift for the Alligator Jaw
int TeethPeriod = 8; // Default period for the Alligator Teeth
int TeethShift = 5; // Default shift for the Alligator Teeth
int LipsPeriod = 5; // Default period for the Alligator Lips
int LipsShift = 3; // Default shift for the Alligator Lips
ENUM_MA_METHOD MaMethod = MODE_SMA; // Default moving average method for Alligator

// RSI input parameter
int RSIPeriod = 14; // Default value for RSI period

// Structure to hold market data including indicators
struct MarketData
{
    datetime time; // Time of the bar
    double open; // Open price
    double high; // High price
    double low; // Low price
    double close; // Close price
    long volume; // Volume (tick volume)
    double movingAverage; // Moving Average data
    double alligatorJaw; // Alligator Jaw
    double alligatorTeeth; // Alligator Teeth
    double alligatorLips; // Alligator Lips
    double rsi; // RSI data
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
    if (GlobalVariableCheck("RSIPeriod"))
        RSIPeriod = GlobalVariableGet("RSIPeriod");

    // Retrieve Alligator parameters from global variables
    if (GlobalVariableCheck("JawPeriod"))
        JawPeriod = GlobalVariableGet("JawPeriod");
    if (GlobalVariableCheck("JawShift"))
        JawShift = GlobalVariableGet("JawShift");
    if (GlobalVariableCheck("TeethPeriod"))
        TeethPeriod = GlobalVariableGet("TeethPeriod");
    if (GlobalVariableCheck("TeethShift"))
        TeethShift = GlobalVariableGet("TeethShift");
    if (GlobalVariableCheck("LipsPeriod"))
        LipsPeriod = GlobalVariableGet("LipsPeriod");
    if (GlobalVariableCheck("LipsShift"))
        LipsShift = GlobalVariableGet("LipsShift");
    if (GlobalVariableCheck("MaMethod"))
        MaMethod = GlobalVariableGet("MaMethod");

    // Print debug information
    Print("BarsToRetrieve: ", BarsToRetrieve);
    Print("Timeframe: ", Timeframe);
    Print("MovingAveragePeriod: ", MovingAveragePeriod);
    Print("RSIPeriod: ", RSIPeriod);
    Print("JawPeriod: ", JawPeriod);
    Print("JawShift: ", JawShift);
    Print("TeethPeriod: ", TeethPeriod);
    Print("TeethShift: ", TeethShift);
    Print("LipsPeriod: ", LipsPeriod);
    Print("LipsShift: ", LipsShift);
    Print("MaMethod: ", MaMethod);

    // Validate parameters
    if (BarsToRetrieve <= 0 || MovingAveragePeriod <= 0 || RSIPeriod <= 0 || JawPeriod <= 0 || TeethPeriod <= 0 || LipsPeriod <= 0)
    {
        Print("Invalid parameters: One or more periods are less than or equal to 0");
        return;
    }

    // Retrieve and combine data
    MarketData marketDataArray[]; // Array to hold market data
    double ma[]; // Array to hold moving average values
    double alligatorJaw[]; // Array to hold Alligator Jaw values
    double alligatorTeeth[]; // Array to hold Alligator Teeth values
    double alligatorLips[]; // Array to hold Alligator Lips values
    double rsi[]; // Array to hold RSI values
    MqlRates rates[]; // Array to hold rates data
    ArraySetAsSeries(ma, true); // Set array as series
    ArraySetAsSeries(alligatorJaw, true); // Set array as series
    ArraySetAsSeries(alligatorTeeth, true); // Set array as series
    ArraySetAsSeries(alligatorLips, true); // Set array as series
    ArraySetAsSeries(rsi, true); // Set array as series
    ArraySetAsSeries(rates, true); // Set array as series
    int copiedRates = CopyRates(Symbol(), Timeframe, 0, BarsToRetrieve, rates); // Copy rates data
    
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

    // Get the handle to the Alligator indicator
    int alligatorHandle = iAlligator(Symbol(), Timeframe, JawPeriod, JawShift, TeethPeriod, TeethShift, LipsPeriod, LipsShift, MaMethod, PRICE_MEDIAN);
    if (alligatorHandle == INVALID_HANDLE)
    {
        Print("Failed to create Alligator handle");
        return;
    }

    // Copy the Alligator values into the respective arrays
    int copiedAlligatorJaw = CopyBuffer(alligatorHandle, 0, 0, BarsToRetrieve, alligatorJaw);
    int copiedAlligatorTeeth = CopyBuffer(alligatorHandle, 1, 0, BarsToRetrieve, alligatorTeeth);
    int copiedAlligatorLips = CopyBuffer(alligatorHandle, 2, 0, BarsToRetrieve, alligatorLips);
    if (copiedAlligatorJaw <= 0 || copiedAlligatorTeeth <= 0 || copiedAlligatorLips <= 0)
    {
        Print("Failed to copy Alligator values");
        return;
    }

    // Get the handle to the RSI indicator
    int rsiHandle = iRSI(Symbol(), Timeframe, RSIPeriod, PRICE_CLOSE);
    if (rsiHandle == INVALID_HANDLE)
    {
        Print("Failed to create RSI handle");
        return;
    }

    // Copy the RSI values into the rsi array
    int copiedRSI = CopyBuffer(rsiHandle, 0, 0, BarsToRetrieve, rsi);
    if (copiedRSI <= 0)
    {
        Print("Failed to copy RSI values");
        return;
    }

    // Check if arrays are not empty before accessing their elements
    if (ArraySize(alligatorJaw) > 0)
        Print("Alligator Jaw: ", alligatorJaw[0]);
    else
        Print("Alligator Jaw array is empty");

    if (ArraySize(alligatorTeeth) > 0)
        Print("Alligator Teeth: ", alligatorTeeth[0]);
    else
        Print("Alligator Teeth array is empty");

    if (ArraySize(alligatorLips) > 0)
        Print("Alligator Lips: ", alligatorLips[0]);
    else
        Print("Alligator Lips array is empty");

    if (ArraySize(rsi) > 0)
        Print("RSI: ", rsi[0]);
    else
        Print("RSI array is empty");

    // Combine rates and indicator data into marketDataArray
    for(int i = 0; i < copiedRates; i++)
    {
        MarketData data;
        data.time = rates[i].time;
        data.open = rates[i].open;
        data.high = rates[i].high;
        data.low = rates[i].low;
        data.close = rates[i].close;
        data.volume = rates[i].tick_volume; // No conversion needed
        data.movingAverage = (i < ArraySize(ma)) ? ma[i] : 0.0;
        data.alligatorJaw = (i < ArraySize(alligatorJaw)) ? alligatorJaw[i] : 0.0;
        data.alligatorTeeth = (i < ArraySize(alligatorTeeth)) ? alligatorTeeth[i] : 0.0;
        data.alligatorLips = (i < ArraySize(alligatorLips)) ? alligatorLips[i] : 0.0;
        data.rsi = (i < ArraySize(rsi)) ? rsi[i] : 0.0;
        ArrayResize(marketDataArray, ArraySize(marketDataArray) + 1);
        marketDataArray[ArraySize(marketDataArray) - 1] = data;
    }

    // Write data to CSV file
    int file_handle = FileOpen("MarketData.csv", FILE_WRITE|FILE_CSV|FILE_COMMON);
    if(file_handle != INVALID_HANDLE)
    {
        // Write header
        FileWrite(file_handle, "Time,Open,High,Low,Close,Volume,MovingAverage,AlligatorJaw,AlligatorTeeth,AlligatorLips,RSI");
        // Write data
        for(int i = 0; i < ArraySize(marketDataArray); i++)
        {
            MarketData data = marketDataArray[i];
            FileWrite(file_handle, TimeToString(data.time, TIME_DATE|TIME_MINUTES), 
                      data.open, data.high, data.low, data.close, data.volume, 
                      data.movingAverage, data.alligatorJaw, data.alligatorTeeth, data.alligatorLips, data.rsi);
        }
        FileClose(file_handle);
        Print("Data written to MarketData.csv");
    }
    else
    {
        Print("Failed to open file for writing");
    }
}