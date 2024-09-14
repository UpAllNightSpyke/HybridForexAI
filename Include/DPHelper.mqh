//+------------------------------------------------------------------+
//|                                                     DPHelper.mqh |
//|                                  Copyright 2024, UpAllNightSpyke |
//|                                  https://www.UpAllNightSpyke.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, UpAllNightSpyke"
#property link      "https://www.UpAllNightSpyke.com"
//+------------------------------------------------------------------+
//| defines                                                          |
//+------------------------------------------------------------------+
#ifndef __DPHELPER_MQH__
#define __DPHELPER_MQH__

// Include necessary libraries
//*********************************************Update to real folder when in production**********************************************
#include "Trade/Trade.mqh"
#include "DPGlobals.mqh" //*********************************************Update to real folder when in production**********************************************


//+////////////////////////////////////////////////////////////////+//
//---------------Basic Operation Functions---------------------------+
//+////////////////////////////////////////////////////////////////+//

//+------------------------------------------------------------------+
//|     Search Patterns                                              |
//+------------------------------------------------------------------+
int SearchPatterns(vector &SearchVectorA, int ValueSearchedA, vector &SearchVectorB, int ValueSearchedB)
  {
   int count = 0;
   for(ulong i = 0; i < SearchVectorA.Size(); i++)
     {
      if(SearchVectorA[i] == ValueSearchedA && SearchVectorB[i] == ValueSearchedB)
         count++;
     }
   return count;
  }

//+------------------------------------------------------------------+
//|     Prevent Division By ZERO                                     |
//+------------------------------------------------------------------+
double CheckZero(double x)
  {
   return x == 0 ? 1.0 : x;
  }

//+////////////////////////////////////////////////////////////////+//
//---------Matrix And Vector Manipulation Functions------------------+
//+////////////////////////////////////////////////////////////////+//

//+------------------------------------------------------------------+
//|     Vector To Matrix                                             |
//+------------------------------------------------------------------+
matrix VectorToMatrix(const vector &v, ulong cols = 1) {
   ulong rows = 0;
   matrix mat = {};

   // Check if the number of columns is valid
   if (v.Size() % cols > 0) {
      printf(__FUNCTION__, " Invalid num Of cols for new matrix. Vector size: %lu, cols: %lu", v.Size(), cols);
      return mat;
   }

   rows = v.Size() / cols;
   mat.Resize(rows, cols);

   // Fill the matrix with values from the vector
   for (ulong i = 0, index = 0; i < rows; i++) {
      for (ulong j = 0; j < cols; j++, index++) {
         mat[i][j] = v[index];
      }
   }

   // Print matrix size for debugging
   printf(__FUNCTION__, " Matrix size: %lux%lu", rows, cols);

   return mat;
}
/* matrix VectorToMatrix(const vector &v, ulong cols = 1)
  {
   ulong rows = 0;
   matrix mat = {};

   if(v.Size()%cols > 0)
     {
      printf(__FUNCTION__, "Invalid num Of cols for new matrix");
      return mat;
     }

   rows = v.Size() / cols;
   mat.Resize(rows, cols);

   for(ulong i = 0, index = 0; i < rows; i++)
      for(ulong j = 0; j < cols; j++, index++)
         mat[i][j] = v[index];

   return mat;
  } */

//+------------------------------------------------------------------+
//|     Matrix to Vector                                             |
//+------------------------------------------------------------------+
vector MatrixToVector(const matrix &Mat)
  {
   vector v = {};

   if(!v.Assign(Mat))
      Print(__FUNCTION__, "Failed converting a matrix to a vector");
   return v;
  }

//+------------------------------------------------------------------+
//|     Convert Array to use in Col function                         |
//+------------------------------------------------------------------+
void ColFromArray(double &array[], int colIndex)
  {
   int size = ArraySize(array);
   for(int i = 0; i < size; ++i)
     {
      InputMatrix[i][colIndex] = array[i];
     }
  }

//+------------------------------------------------------------------+
//|     Min/Max Normalization                                        |
//+------------------------------------------------------------------+
void MinMaxNormalization(matrix &Matrix)
  {
   vector column;
   for(ulong i = 0; i < InputNumCol; i++)
     {
      column = Matrix.Col(i);
      MinMaxNorm.min[i] = column.Min();
      MinMaxNorm.max[i] = column.Max();
      column = (column - MinMaxNorm.min[i]) / (MinMaxNorm.max[i] - MinMaxNorm.min[i]);
      Matrix.Col(column, i);
     }
  }

//+------------------------------------------------------------------+
//|     Removing Index From Vector                                   |
//+------------------------------------------------------------------+
void VectorRemoveIndex(vector &v,ulong index)
  {
//creates new vector with 1 index value shorter
   vector new_v(v.Size()-1);
//This loop will create a variable count and loop through original vector while i != index. Then the new vector new_v[count] will be the original vector at index i
   for(ulong i=0,count=0; i<v.Size(); i++)
     {
      if(i!=index)
        {
         new_v[count] = v[i];
         count++;
        }
     }
   v.Copy(new_v);
  }

//+------------------------------------------------------------------+
//|     Remove Column From Matrix                                    |
//+------------------------------------------------------------------+
void MatrixRemoveCol(matrix &mat,ulong col)
  {
//remember Rows() and Cols() return the count of the rows/columns. this is different that Row()  and Col() which access the matrix.
   matrix new_matrix(mat.Rows(),mat.Cols()-1);
   for(ulong i=0,new_col=0; i<mat.Cols(); i++)
     {
      // if the i = col that means the index is at the proper column. otherwise we continue to loop until the new_col is at the index i
      if(i==col)
         continue;
      else
        {
         new_matrix.Col(mat.Col(i),new_col);
         new_col++;
        }
     }
   mat.Copy(new_matrix);
  }

//+------------------------------------------------------------------+
//|      Remove Row From Matrix                                      |
//+------------------------------------------------------------------+
void MatrixRemoveRow(matrix &mat,ulong row)
  {
   matrix new_matrix(mat.Rows()-1,mat.Cols());
   for(ulong i=0,new_rows=0; i<mat.Cols(); i++)
     {
      // if the i = col that means the index is at the proper column. otherwise we continue to loop until the new_col is at the index i
      if(i==row)
         continue;
      else
        {
         new_matrix.Row(mat.Row(i),new_rows);
         new_rows++;
        }
     }
   mat.Copy(new_matrix);
  }

//+------------------------------------------------------------------+
//|     Remove Duplicate Index Maintain Appearance Order             |
//+------------------------------------------------------------------+
vector Classes(vector &v)//removes duplicates and places new vector in temp vector to avoid changing base data
  {
//the 2 vectors, temp_t to avoid changing original vector, and v_classes initialized by first element of vector_v
   vector temp_t = v,v_classes = {v[0]};
   for(ulong i=0, count =1; i<v.Size(); i++)
     {
      for(ulong j=0; j<v.Size(); j++)
        {
         if(v[i] == temp_t[j] && temp_t[j] != -1000)
           {
            bool count_ready = false;
            //this loop will go through the vector and if duplicate values from v[i] are found mark it with -1000 as already copied
            for(ulong n=0; n<v_classes.Size(); n++)
               if(v[i] == v_classes[n])
                  count_ready = true;
            if(!count_ready)
              {
               count++;
               v_classes.Resize(count);
               v_classes[count-1] = v[i];
               temp_t[j] = -1000;
              }
            else
               break;
           }
         else
            continue;
        }
     }
   return v_classes;
  }

//+------------------------------------------------------------------+
//|     One Hot Encoding                                             |
//+------------------------------------------------------------------+
matrix OneHotEncoding(vector &v) //Converts categorical data (non numeric) to numeric values
  {
   matrix mat = {};
   vector v_classes = Classes(v);//deriving different categories to be used in function
   mat.Resize(v.Size(),v_classes.Size());// resized matrix to hold the vector and the categorical/classification data
   mat.Fill(-100); //Placeholder Value

   for(ulong i=0; i<mat.Rows(); i++)
     {
      for(ulong j=0; j<mat.Cols(); j++)
        {
         if(v[i]==v_classes[j]) //if an element belongs to the class of the row, the column will be marked with 1 and the rest of the columns in the row 0

            mat[i][j] = 1;

         //one hot encoding example vector = {red,blue,grey,red,grey}
         //red|blue|grey|
         //[1]  [0]  [0]
         //[0]  [1]  [0]
         //[0]  [0]  [1]
         //[1]  [0]  [0]
         //[0]  [0]  [1]
         else
            mat[i][j] = 0;
        }
     }
   return mat;
  }

//+////////////////////////////////////////////////////////////////+//
//---------------Neural Network functions----------------------------+
//+////////////////////////////////////////////////////////////////+//

////+------------------------------------------------------------------+
////|     Neuron Function                                              |
////+------------------------------------------------------------------+
//matrix Neuron(matrix &I, matrix &W, matrix &B, ENUM_ACTIVATION_FUNCTION Activation)
//  {
//   matrix OutPuts;
//   ((W.MatMul(I)) + B).Activation(OutPuts, Activation);
//   return OutPuts;
//  }

////+------------------------------------------------------------------+
////|     Single Input Forward Pass                                    |
////+------------------------------------------------------------------+
//matrix SingleInputForwardPass(vector &input_v)
//  {
//   vector temp_x = input_v;
//
//   if(!BPDone)
//      BPMinMaxNormalization(temp_x);
//
//   matrix INPUT = VectorToMatrix(temp_x);
//   return Neuron(INPUT, Weights, Bias, ENUM_ACTIVATION_FUNCTION(ActivationFx));
//  }
//
////+------------------------------------------------------------------+
////|     Live Forward Pass                                            |
////+------------------------------------------------------------------+
//vector LiveForwardPass(vector &input_v)
//  {
//   matrix ret_mat = SingleInputForwardPass(input_v);
//   return MatrixToVector(ret_mat);
//  }
//
////+------------------------------------------------------------------+
////|     Batched Data Forward Pass                                    |
////+------------------------------------------------------------------+
//vector BatchInputForwardPass(matrix &x_matrix)
//  {
//   vector ret(x_matrix.Rows());
//   matrix OutPuts;
//   vector v = {};
//   for(ulong i = 0; i < x_matrix.Rows(); i++)
//     {
//      v = LiveForwardPass(x_matrix.Row(i));
//      ret[i] = ClassesVector[(int)v.ArgMax()];
//     }
//   return ret;
//  }
//
////+------------------------------------------------------------------+
////|     Back Propagation Vector To Matrix                            |
////+------------------------------------------------------------------+
//void BPMinMaxNormalization(vector &v) //function needs a vector and vectors are passed in as references. Reference by stating (vector &v) preventing original data loss
//  {
//   if(v.Size()!=InputNumCol) //Ensures vector is same size as the matrix columns
//     {
//      Print("Cant Normalize the data, Vector size must be = the size fo the matrix columns");
//      return;
//     }
//   for(ulong i=0; i<InputNumCol; i++) //iterates through each vector data point and normalizes data.
//      v[i] = (v[i]-MinMaxNorm.min[i])/(MinMaxNorm.max[i]-MinMaxNorm.min[i]);
//  }
//

#endif // __DPHELPER_MQH__
//+------------------------------------------------------------------+
