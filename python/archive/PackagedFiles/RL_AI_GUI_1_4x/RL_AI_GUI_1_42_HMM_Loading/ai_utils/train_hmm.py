from hmmlearn import hmm

import pandas as pd
from appdirs import user_data_dir
import os
import pickle

def find_raw_data():
    """
    Locates the raw data file in the user data directory.

    Returns:
        str: The path to the raw data file.

    Raises:
        FileNotFoundError: If no raw data file is found.
    """
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
    raw_data_dir = os.path.join(user_data_path, 'forex_data', 'raw')

    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".csv"):  # Assuming raw data files end with ".csv"
            raw_data_file = os.path.join(raw_data_dir, filename)
            return raw_data_file

    raise FileNotFoundError("No raw data file found.")

def train_hmm_model():
    """
    Trains the HMM model using the raw data with NaN removal and saves it in the HMMmodel directory.
    """
    try:
        # 1. Load the raw data
        raw_data_file = find_raw_data()
        data = pd.read_csv(raw_data_file)

        # 2. Remove rows with NaN values
        data.dropna(inplace=True)

        # 3. Feature engineering for time-based features (using datetime)
        data['time'] = pd.to_datetime(data['time'])  # Convert to datetime objects
        data['hour_of_day'] = data['time'].dt.hour
        data['day_of_week'] = data['time'].dt.dayofweek
        # ... add other time-based features as needed ...

        # 4. Select relevant columns for HMM training (including time features)
        hmm_data = data[['open', 'high', 'low', 'close', 'tick_volume',
                         'hour_of_day', 'day_of_week']].values

        # 5. Create and train the HMM model
        model = hmm.GaussianHMM(n_components=3,
                                covariance_type="full", n_iter=100)
        model.fit(hmm_data)

        # 6. Save the trained HMM model in the HMMmodel directory
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'HMMmodel')
        os.makedirs(model_dir, exist_ok=True)
        model_filename = os.path.join(model_dir, 'hmm_model.pkl')
        with open(model_filename, 'wb') as file:
            pickle.dump(model, file)

        print("HMM trained and saved successfully!")
    except Exception as e:
        print(f"An error occurred while training the HMM: {e}")

def load_hmm_model():
    """
    Loads the trained HMM model from the HMMmodel directory.

    Returns:
        hmmlearn.hmm.GaussianHMM: The trained HMM model.

    Raises:
        FileNotFoundError: If the HMM model file is not found.
    """
    try:
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'HMMmodel')
        model_filename = os.path.join(model_dir, 'hmm_model.pkl')
        with open(model_filename, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        print("Trained HMM model not found.")
        return None