import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

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

def load_raw_data(file_path):
    """
    Load the raw data from a file.
    """
    return pd.read_csv(file_path)

def preprocess_data(data):
    """
    Perform initial preprocessing steps.
    Example: cleaning, normalization, feature engineering.
    """
    # Example preprocessing: normalize the 'close' column
    data['normalized_close'] = (data['close'] - data['close'].mean()) / data['close'].std()
        
    # Ensure 'volume' column is included in the preprocessing
    if 'volume' not in data.columns:
        raise KeyError("'volume' column is missing from the raw data")
    
    # Include additional columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"'{col}' column is missing from the raw data")
    
    # Select only the required columns
    data = data[required_columns]
    
    return data

def save_preprocessed_data(data, file_path):
    """
    Save the preprocessed data to a file.
    """
    data.to_csv(file_path, index=False)

def load_prepared_data(file_path):
    """
    Load and preprocess the data from the given file path.
    """
    # Read the file with a specified encoding
    data = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    print("Successfully loaded prepared data.")
    return data

def select_top_features(data, target_column='Close', num_features=9):
    """
    Select the top features based on feature importance using a RandomForestRegressor.
    """
    features = data.drop(columns=[target_column])
    target = data[target_column]

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(features, target)
    feature_importance = pd.Series(rf.feature_importances_, index=features.columns).sort_values(ascending=False)
    top_features = feature_importance.head(num_features).index.tolist()
    if target_column not in top_features:
        top_features.append(target_column)
    selected_data = data[top_features]
    return selected_data