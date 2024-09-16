//+------------------------------------------------------------------+
//|                                               DataCollectEA1_01.mq5 |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                 https://www.upallnightspyke.com/ |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.upallnightspyke.com/"
#property version   "1.01"

// Input parameters
input int BarsToRetrieve = 100;            // Number of bars to retrieve
input ENUM_TIMEFRAMES Timeframe = PERIOD_H1; // Timeframe for data retrieval
input int MovingAveragePeriod = 14;        // Period for the moving average
input int RSIPeriod = 14;                  // Period for the RSI

// Alligator input parameters
input int JawPeriod = 13; // Period for the Alligator Jaw
input int JawShift = 8; // Shift for the Alligator Jaw
input int TeethPeriod = 8; // Period for the Alligator Teeth
input int TeethShift = 5; // Shift for the Alligator Teeth
input int LipsPeriod = 5; // Period for the Alligator Lips
input int LipsShift = 3; // Shift for the Alligator Lips
input ENUM_MA_METHOD MaMethod = MODE_SMA; // Moving average method for Alligator

void OnTick()
{
    // Set global variables
    GlobalVariableSet("BarsToRetrieve", BarsToRetrieve);
    GlobalVariableSet("Timeframe", Timeframe);
    GlobalVariableSet("MovingAveragePeriod", MovingAveragePeriod);
    GlobalVariableSet("RSIPeriod", RSIPeriod);

    // Set Alligator parameters as global variables
    GlobalVariableSet("JawPeriod", JawPeriod);
    GlobalVariableSet("JawShift", JawShift);
    GlobalVariableSet("TeethPeriod", TeethPeriod);
    GlobalVariableSet("TeethShift", TeethShift);
    GlobalVariableSet("LipsPeriod", LipsPeriod);
    GlobalVariableSet("LipsShift", LipsShift);
    GlobalVariableSet("MaMethod", MaMethod);

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

    // Trigger the script using a chart event
    long chart_id = ChartID();
    EventChartCustom(chart_id, 0, 0, 0, 0);

    // Remove the EA after triggering the script
    ExpertRemove();
}