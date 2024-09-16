# Project Scope and Detailed Plan

## Objective
Develop a Hybrid Reinforcement Learning (RL) AI system for forex trading that:
1. Collects and processes live data from MetaTrader 5 (MT5) using MQL5 scripts.
2. Uses Python scripts to preprocess data, train and update the RL model, and perform hyperparameter tuning.
3. Utilizes a C++ program to make real-time predictions based on the trained model and live data.

## Components
1. **MQL5 Scripts (MT5)**
2. **Python Scripts**
3. **C++ Program**

## Steps and Functionality

### 1. MQL5 Scripts (MT5)
**Functionality:**
- Collect live forex data, including symbol information, indicators, and other metrics.
- Save the collected data to a TSV file for further processing.

**Steps:**
1. Write MQL5 scripts to gather live data from MT5.
2. Save the data to a TSV file (`MarketData.tsv`).

### 2. Python Scripts
**Functionality:**
- Preprocess the collected data.
- Train and update the RL model.
- Perform hyperparameter tuning.
- Save the trained model for use in the C++ program.

**Steps:**
1. **Data Preparation:**
   - **Script:** `data_preparation.py`
   - **Functionality:** Load, clean, and normalize data from the TSV file. Save the prepared data to a new TSV file (`PreparedModelData.tsv`).

2. **Model Training:**
   - **Script:** `model_training.py`
   - **Functionality:** Load the prepared data, split it into training and testing sets, train a Random Forest model, and evaluate its performance using metrics like Mean Squared Error (MSE) and R² Score.

3. **Hyperparameter Tuning:**
   - **Script:** `GridSearchModeling1_00.py`
   - **Functionality:** Perform hyperparameter tuning using GridSearchCV to find the best parameters for the model. Save the best model to `best_model.joblib`.

4. **Periodic Model Updates:**
   - **Script:** `periodic_model_update.py`
   - **Functionality:** Periodically retrain the model with new data collected by the C++ program and save the updated model to a shared location.

### 3. C++ Program
**Functionality:**
- Collect live data from MT5 or other sources.
- Load the pre-trained model and make real-time predictions.
- Periodically check for updated models and reload them.

**Steps:**
1. **Real-time Data Collection and Prediction:**
   - **Functionality:** Collect live data, preprocess it, and save it to a shared location (e.g., CSV file). Use the TensorFlow C++ API to load the pre-trained model and make predictions on the live data.

2. **Model Reloading:**
   - **Functionality:** Periodically check for updated models and reload them to ensure the latest model is used for predictions.

## Summary of Accomplishments

### Data Preparation
- Created a script (`data_preparation.py`) to load, clean, and normalize data from a TSV file.
- Saved the prepared data to a new TSV file (`PreparedModelData.tsv`).

### Model Training
- Created a script (`model_training.py`) to load the prepared data, split it into training and testing sets, train a Random Forest model, and evaluate its performance.
- Evaluated the model using Mean Squared Error (MSE) and R² Score.

### Hyperparameter Tuning
- Created a new script (`GridSearchModeling1_00.py`) to perform hyperparameter tuning using GridSearchCV.
- Found the best hyperparameters for the Random Forest model and evaluated its performance.
  - **Best Parameters:** `{'max_depth': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 50}`
  - **Model Performance:** `Mean Squared Error: 0.00014814345890900302`, `R^2 Score: 0.9952321842174128`

### Model Persistence
- Updated the `GridSearchModeling1_00.py` script to save the trained model to disk using `joblib`.
- Checked the size of the saved model file.

### File Paths and Directories
- Ensured the prepared data and model files were saved to appropriate directories.
- Updated the `.gitignore` file to ignore the `venv/` and `models/` directories to avoid pushing them to the repository.

### Key Files Created/Updated
1. **data_preparation.py**
   - Loads, cleans, and normalizes data from a TSV file.
   - Saves the prepared data to `PreparedModelData.tsv`.

2. **model_training.py**
   - Loads prepared data, trains a Random Forest model, and evaluates its performance.

3. **GridSearchModeling1_00.py**
   - Performs hyperparameter tuning using GridSearchCV.
   - Saves the best model to `best_model.joblib`.
   - Prints the size of the saved model file.

4. **.gitignore**
   - Updated to ignore `venv/` and `models/` directories.

### Commands Used
1. **Running Data Preparation Script:**
   ```sh
   python data_preparation.py