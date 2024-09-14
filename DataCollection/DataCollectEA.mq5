//+------------------------------------------------------------------+
//|                                               DataCollectionEA.mq5 |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                 https://www.upallnightspyke.com/ |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.upallnightspyke.com/"
#property version   "1.00"

// Input parameters
input int BarsToRetrieve = 100;            // Number of bars to retrieve
input ENUM_TIMEFRAMES Timeframe = PERIOD_H1; // Timeframe for data retrieval
input int MovingAveragePeriod = 14;        // Period for the moving average

void OnTick()
{
    // Set global variables
    GlobalVariableSet("BarsToRetrieve", BarsToRetrieve);
    GlobalVariableSet("Timeframe", Timeframe);
    GlobalVariableSet("MovingAveragePeriod", MovingAveragePeriod);

    // Print debug information
    Print("BarsToRetrieve: ", BarsToRetrieve);
    Print("Timeframe: ", Timeframe);
    Print("MovingAveragePeriod: ", MovingAveragePeriod);

    // Trigger the script using a chart event
    long chart_id = ChartID();
    EventChartCustom(chart_id, 0, 0, 0, 0);

    // Remove the EA after triggering the script
    ExpertRemove();
}