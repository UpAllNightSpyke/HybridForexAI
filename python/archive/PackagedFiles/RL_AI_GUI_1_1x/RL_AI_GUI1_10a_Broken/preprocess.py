import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

def preprocess_observation(observation):
    """
    Preprocess the observation before passing it to the agent.
    For example, normalize the observation.
    """
    return observation / 255.0

def preprocess_action(action):
    """
    Preprocess the action before passing it to the environment.
    For example, discretize continuous actions.
    """
    # Assuming action is already discrete, so no preprocessing needed
    return action

def load_prepared_data(file_path, time_format='int'):
    """
    Load and preprocess the data from the given file path.
    """
    print(f"Loading data from {file_path}...")  # Debug line
    data = pd.read_csv(file_path, sep='\t')
    print(f"Columns in the loaded data: {data.columns}")  # Debug line
    
    # Convert 'time' column to Unix timestamp in seconds
    data['time'] = pd.to_datetime(data['time']).astype('int64') // 10**9
    print(f"Data types after conversion: {data.dtypes}")  # Debug line

    print("Successfully loaded prepared data.")
    return data

def select_top_features(data, target_column='close', num_features=9):
    """
    Select the top features based on feature importance using a RandomForestRegressor.
    """
    features = data.drop(columns=['time', target_column])
    target = data[target_column]
    
    # Handle NaN values
    imputer = SimpleImputer(strategy='mean')
    features = imputer.fit_transform(features)
    
    # Remove columns with no observed values
    valid_columns = [col for col in data.drop(columns=['time', target_column]).columns if col in data.columns and data[col].notna().any()]
    features = pd.DataFrame(features, columns=valid_columns)
    
    # Log the columns and their NaN status
    print("Columns after imputation and filtering:")
    for col in valid_columns:
        print(f"{col}: NaN count = {data[col].isna().sum()}")
    
    rf = RandomForestRegressor()
    rf.fit(features, target)
    
    importances = rf.feature_importances_
    feature_names = features.columns
    
    # Ensure feature_names and importances have the same length
    if len(feature_names) != len(importances):
        raise ValueError("Mismatch between feature names and importances lengths")
    
    feature_importances = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feature_importances = feature_importances.sort_values(by='importance', ascending=False)
    
    top_features = feature_importances['feature'].head(num_features).tolist()
    selected_data = data[['time', target_column] + top_features]
    
    # Check for NaN values in the selected data
    if selected_data.isna().any().any():
        print("NaN values found in the selected data:")
        print(selected_data.isna().sum())
        raise ValueError("NaN values found in the selected data")
    
    return selected_data

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python preprocess.py <file_path>")
    else:
        file_path = sys.argv[1]
        data = load_prepared_data(file_path)
        selected_data = select_top_features(data)
        print("Preprocessing completed successfully.")