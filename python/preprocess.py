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

def load_prepared_data(file_path):
    """
    Load and preprocess the data from the given file path.
    """
    # Read the file with a specified encoding
    data = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    print("Successfully loaded prepared data.")
    return data

def select_top_features(data, target_column='close', num_features=9):
    """
    Select the top features based on feature importance using a RandomForestRegressor.
    """
    # Ensure the date column is removed or converted
    if 'time' in data.columns:
        data['time'] = pd.to_datetime(data['time'])
        data['time'] = data['time'].map(pd.Timestamp.timestamp)  # Convert to timestamp

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