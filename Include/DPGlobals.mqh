//+------------------------------------------------------------------+
//|                                                    DPGlobals.mqh |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                  https://www.UpAllNightSpyke.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.UpAllNightSpyke.com"
//+------------------------------------------------------------------+
//| defines                                                          |
//+------------------------------------------------------------------+
#ifndef __DPGLOBALS_MQH__
#define __DPGLOBALS_MQH__

// Include necessary libraries
#include "Trade/Trade.mqh"

//+////////////////////////////////////////////////////////////////+//
//---------------Global Extern Variables-----------------------------+
//+////////////////////////////////////////////////////////////////+//

extern int OldNumBars;

extern ulong InputNumCol;

vector ClassesVector;

extern matrix InputMatrix, Weights, Bias;

extern bool BPDone; //boolean for training status


//+////////////////////////////////////////////////////////////////+//
//---------------Global Extern Structures----------------------------+
//+////////////////////////////////////////////////////////////////+//

struct NormalizationStructure //Creates the structure that holds the minimum and maximum values of our data. Structure creates objects with 1 input: Columns
  {
   vector            min;
   vector            max;
                     NormalizationStructure::NormalizationStructure(ulong Columns)
     {
      min.Resize(Columns);    //part of structure that stores min/max values
      max.Resize(Columns);    //resizing to ensure that the sizes match

     }
  } MinMaxNorm(InputNumCol);  //creates object to access data


#endif // __DPGLOBALS_MQH__